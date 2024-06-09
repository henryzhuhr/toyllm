import argparse
import time
from threading import Thread
from sympy import comp
from optimum.intel.openvino import (
    OVModelForCausalLM,
    OVWeightQuantizationConfig,
)
from transformers import (
    AutoTokenizer,
    AutoConfig,
    TextIteratorStreamer,
    StoppingCriteriaList,
    PreTrainedTokenizer,
)
import openvino as ov

from utils.llm_config import SUPPORTED_LLM_LIST, SupportedLLMConfig
from utils.llm_utils import StopOnTokens, convert_history_to_token, parse_text


class InferArgs:

    def get_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-m", "--model_id", type=str, default="Qwen/Qwen2-7B"
        )
        parser.add_argument(
            "-p",
            "--model_path",
            type=str,
            default="weights/Qwen/Qwen2-7B-IR-int8",
        )
        parser.add_argument("--max_sequence_length", type=int, default=256)
        parser.add_argument("--device", type=str, default="CPU")
        return parser.parse_args()

    def __init__(self) -> None:
        args = self.get_args()
        self.model_id: str = args.model_id
        self.model_path: str = args.model_path
        self.max_sequence_length: str = args.max_sequence_length
        self.device: str = args.device


def main():
    args = InferArgs()
    core = ov.Core()
    print("-- [INFO] Available Devices:", core.available_devices)

    st = time.time()
    tokenizer: PreTrainedTokenizer = AutoTokenizer.from_pretrained(
        args.model_path, trust_remote_code=True
    )
    print(f"-- [INFO] Tokenizer Load Time: {time.time() - st:.2f} s")
    ov_config = {
        # "KV_CACHE_PRECISION": "u8", "DYNAMIC_QUANTIZATION_GROUP_SIZE": "32",  # BUG: error in GPU
        "PERFORMANCE_HINT": "LATENCY",
        "NUM_STREAMS": "1",
        "CACHE_DIR": ".cache",
    }
    st = time.time()
    ov_model = OVModelForCausalLM.from_pretrained(
        args.model_path,
        device=args.device,
        ov_config=ov_config,
        config=AutoConfig.from_pretrained(
            args.model_path, trust_remote_code=True
        ),
        trust_remote_code=True,
        quantization_config=OVWeightQuantizationConfig(bits=4),
        use_cache=True,
        compile=False,
        export=False,
    )
    print(f"-- [INFO] {args.model_id} Load Time: {time.time() - st:.2f} s")
    st = time.time()
    ov_model.compile()
    print(f"-- [INFO] {args.model_id} Compile Time: {time.time() - st:.2f} s")
    model_config: SupportedLLMConfig = None
    for sli in SUPPORTED_LLM_LIST:
        if sli.model_id == args.model_id:
            model_config = sli
            break
    start_message = model_config.model_kwargs["start_message"]
    stop_tokens = model_config.model_kwargs["stop_tokens"]
    if stop_tokens is not None:
        if isinstance(stop_tokens[0], str):
            stop_tokens = tokenizer.convert_tokens_to_ids(stop_tokens)
        stop_tokens = [StopOnTokens(stop_tokens)]

    history = []
    input_texts = [
        "你好，你是谁？",
        "你的知识储备到哪一年？",
        "介绍一下西甲联赛以及国家德比",
        "tmd，为什么皇马又拿欧冠冠军了",
    ]

    for input_text in input_texts:
        # while True:
        # input_text = input("用户: ")

        if input_text.lower() == "stop":
            break

        if input_text.lower() == "clear":
            history = []
            print("AI助手: 对话历史已清空")
            continue

        print("用户:", input_text)
        print("AI:", end=" ")
        history = history + [[parse_text(input_text), ""]]
        input_ids = convert_history_to_token(tokenizer, history, start_message)
        if input_ids.shape[1] > 2000:
            history = [history[-1]]
            input_ids = convert_history_to_token(history)
        streamer = TextIteratorStreamer(
            tokenizer, timeout=60.0, skip_prompt=True, skip_special_tokens=True
        )
        generate_kwargs = dict(
            input_ids=input_ids,
            max_new_tokens=args.max_sequence_length,
            temperature=0.1,
            do_sample=True,
            top_p=1.0,
            top_k=50,
            repetition_penalty=1.1,
            streamer=streamer,
            stopping_criteria=StoppingCriteriaList(stop_tokens),
        )

        t1 = Thread(target=ov_model.generate, kwargs=generate_kwargs)
        t1.start()

        partial_text = ""
        for new_text in streamer:
            new_text = new_text
            print(new_text, end="", flush=True)
            partial_text += new_text
        print("\n")
        history[-1][1] = partial_text


if __name__ == "__main__":
    main()

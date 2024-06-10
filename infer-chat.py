import time
import argparse
from typing import List
from threading import Thread
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
        # fmt: off
        parser.add_argument("-m", "--model_id", type=str, default="Qwen/Qwen2-1.5B-Instruct")
        parser.add_argument("-p", "--model_path", type=str, default="weights/Qwen/Qwen2-1.5B-Instruct-IR-int8")
        parser.add_argument("-q", "--quan_type", type=str, default="int8", choices=["fp16", "int8", "int4"])
        parser.add_argument("-l", "--max_sequence_length", type=int, default=256)
        parser.add_argument("-d", "--device", type=str, default="AUTO")
        # fmt: on
        return parser.parse_args()

    def __init__(self) -> None:
        args = self.get_args()
        self.model_id: str = args.model_id
        self.model_path: str = args.model_path
        self.quan_type: str = args.quan_type
        self.max_sequence_length: str = args.max_sequence_length
        self.device: str = args.device


def printc(type: str, *message: List[str]):
    if type == "INFO":
        print(f"\033[00;36m -- [INFO]", *message, "\033[0m")
    elif type == "SUCCESS":
        print(f"\033[00;32m -- [SUCCESS]", *message, "\033[0m")
    elif type == "WARNING":
        print(f"\033[00;33m -- [WARNING]", *message, "\033[0m")
    elif type == "ERROR":
        print(f"\033[00;31m -- [ERROR]", *message, "\033[0m")
    else:
        print(*message)


def main():
    args = InferArgs()
    core = ov.Core()
    printc("INFO", f"Available Devices: {core.available_devices}")

    st = time.time()
    tokenizer: PreTrainedTokenizer = AutoTokenizer.from_pretrained(args.model_path, trust_remote_code=True)
    printc("SUCCESS", f"Tokenizer loaded in {time.time() - st:.2f} s")
    st = time.time()

    ov_config = {
        # ==================
        # -- https://docs.openvino.ai/2024/learn-openvino/llm_inference_guide/llm-inference-hf.html#enabling-openvino-runtime-optimizations
        # -- "[GPU] SDPA indirect inputs": https://github.com/openvinotoolkit/openvino/pull/24665
        # ==================
        "PERFORMANCE_HINT": "LATENCY",
        "NUM_STREAMS": "1",
        "CACHE_DIR": ".cache",
    }
    OVModelForCausalLM_from_pretrained_kwargs = {}
    if args.quan_type == "int4":
        OVModelForCausalLM_from_pretrained_kwargs["quantization_config"] = OVWeightQuantizationConfig(bits=4)
        # ov_config["DYNAMIC_QUANTIZATION_GROUP_SIZE"] = "32"   # BUG: error in GPU
    elif args.quan_type == "int8":
        # BUG: [GPU] Attempt to set user property KV_CACHE_PRECISION (u8) which was not registered or internal!
        # ov_config["KV_CACHE_PRECISION"] = "u8"                # BUG: error in GPU
        # ov_config["DYNAMIC_QUANTIZATION_GROUP_SIZE"] = "32"   # BUG: error in GPU
        pass
    else:
        OVModelForCausalLM_from_pretrained_kwargs = {}

    ov_model: OVModelForCausalLM = OVModelForCausalLM.from_pretrained(
        args.model_path,
        device=args.device,
        ov_config=ov_config,
        config=AutoConfig.from_pretrained(args.model_path, trust_remote_code=True),
        trust_remote_code=True,
        compile=False,
        export=False,
        **OVModelForCausalLM_from_pretrained_kwargs,
    )

    printc("INFO", f"Model '{args.model_id}' Loaded in {time.time() - st:.2f} s")
    st = time.time()
    ov_model.to(args.device)
    ov_model.compile()
    printc("INFO", f"Model '{args.model_id}' Compiled in {time.time() - st:.2f} s")
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
        "介绍一下英特尔公司吧",
        "什么是OpenVINO",
        "OpenVINO有什么优势或者特点",
    ]

    for input_text in input_texts:
        # while True:
        # input_text = input("用户: ")

        if input_text.lower() == "stop":
            break

        if input_text.lower() == "clear":
            history = []
            print("AI Assistant: Conversation history cleared")
            continue

        print(f"\033[00;32m  -- [User]\033[0m", input_text)
        print(f"\033[00;36m  -- [AI Assistant]\033[0m:")

        history = history + [[parse_text(input_text), ""]]
        input_ids = convert_history_to_token(tokenizer, history, start_message)
        if input_ids.shape[1] > 2000:
            history = [history[-1]]
            input_ids = convert_history_to_token(history)
        streamer = TextIteratorStreamer(tokenizer, timeout=60.0, skip_prompt=True, skip_special_tokens=True)
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

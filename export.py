import argparse
import os

from transformers import AutoTokenizer, AutoConfig
from optimum.intel import OVWeightQuantizationConfig
from optimum.intel.openvino import OVModelForCausalLM
from optimum.intel.openvino import (
    OVModelForCausalLM,
    OVWeightQuantizationConfig,
)

from utils.llm_config import SUPPORTED_LLM_LIST, SupportedLLMConfig


class ExportArgs:

    def get_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-m",
            "--model_id",
            type=str,
            default="Qwen/Qwen2-7B",
            choices=[config.model_id for config in SUPPORTED_LLM_LIST],
        )
        parser.add_argument("-s", "--weight_dir", type=str, default=".cache/Qwen/Qwen2-7B")
        parser.add_argument("-q", "--quan_type", type=str, default="int8", choices=["fp16", "int8", "int4"])
        parser.add_argument("-d", "--save_dir", type=str, default="weights")

        return parser.parse_args()

    def __init__(self) -> None:
        args = self.get_args()
        self.model_id: str = args.model_id
        self.weight_dir: str = args.weight_dir
        self.quan_type: str = args.quan_type
        self.save_dir: str = args.save_dir
    model_id_list = [config.model_id for config in SUPPORTED_LLM_LIST]

def main():
    args = ExportArgs()
    llm_config: SupportedLLMConfig = None
    for config in SUPPORTED_LLM_LIST:
        if config.model_id == args.model_id:
            llm_config = config
            break

    # set the export directory
    export_model_dir = os.path.join(args.save_dir, f"{args.model_id}-IR-{args.quan_type}")
    if os.path.exists(export_model_dir):
        print(
            f"\033[00;31m -- [WARNING]\033[0m {export_model_dir} already exists."
            "If you want to overwrite, please delete it manually."
        )
        return 0
    os.makedirs(export_model_dir)

    pretrained_model_name_or_path = args.weight_dir if os.path.exists(args.weight_dir) else args.model_id

    # ============ Tokenizer ==================
    model_kwargs = {
        "trust_remote_code": True,
    }
    tokenizer = AutoTokenizer.from_pretrained(
        pretrained_model_name_or_path,
        **model_kwargs,
    )
    tokenizer.save_pretrained(export_model_dir)
    print(f"\033[00;32m -- [SUCCESS]\033[0m Tokenizer saved to {export_model_dir}")

    # ============ LLM ==================
    config = AutoConfig.from_pretrained(
        pretrained_model_name_or_path,
        trust_remote_code=True,
    )
    print(f"\033[00;32m -- [SUCCESS]\033[0m Load config")
    model_kwargs = {
        "trust_remote_code": True,
        "config": config,
    }
    # cache_dir : https://github.com/huggingface/optimum-intel/issues/347
    if args.quan_type == "int4":
        compression_configs = llm_config.int4_compression_configs
        ov_model = OVModelForCausalLM.from_pretrained(
            pretrained_model_name_or_path,
            export=True,  # compile=False,
            quantization_config=OVWeightQuantizationConfig(bits=4, **compression_configs),
            **model_kwargs,
        )
    elif args.quan_type == "int8":
        ov_model = OVModelForCausalLM.from_pretrained(
            pretrained_model_name_or_path,
            export=True,  # compile=False,
            load_in_8bit=True,
            **model_kwargs,
        )
    else:
        ov_model = OVModelForCausalLM.from_pretrained(
            pretrained_model_name_or_path,
            export=True,  # compile=False,
            load_in_8bit=False,
            **model_kwargs,
        )
    ov_model.save_pretrained(export_model_dir)
    print(f"\033[00;32m -- [SUCCESS]\033[0m LLM Model saved to {export_model_dir}")


if __name__ == "__main__":
    main()

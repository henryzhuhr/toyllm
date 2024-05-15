import argparse
import os

from transformers import AutoTokenizer, AutoConfig
from optimum.intel import OVWeightQuantizationConfig
from optimum.intel.openvino import OVModelForCausalLM
import openvino as ov
import nncf
from optimum.intel.openvino import (
    OVModelForCausalLM,
    OVWeightQuantizationConfig,
)
import gc

from utils.llm_config import SUPPORTED_LLM_LIST, SupportedLLMConfig


class ExportArgs:

    def get_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--model_id",
            type=str,
            default="Qwen/Qwen1.5-1.8B-Chat",
            help="The language of the model to use, divided by a : ,such as English:tiny-llama-1b-chat",
            choices=[config.model_id for config in SUPPORTED_LLM_LIST],
        )
        parser.add_argument(
            "--quan_type",
            type=str,
            default="int4",
            choices=["fp16", "int8", "int4"],
            help="Quantization type to use for the model",
        )
        parser.add_argument(
            "--weight_dir",
            type=str,
            default=".cache",
            help="Output directory to save the model and tokenizer",
        )

        return parser.parse_args()

    def __init__(self) -> None:
        args = self.get_args()
        self.model_id: str = args.model_id
        self.quan_type: str = args.quan_type
        self.weight_dir: str = args.weight_dir


def main():
    args = ExportArgs()
    llm_config: SupportedLLMConfig = None
    for config in SUPPORTED_LLM_LIST:
        if config.model_id == args.model_id:
            llm_config = config
            break

    # set the export directory
    export_model_dir = os.path.join(args.weight_dir, f"{args.model_id}-IR-{args.quan_type}")
    os.makedirs(export_model_dir, exist_ok=True)
    model_kwargs = {
        "trust_remote_code": True,
        # "cache_dir": ".cache",
    }
    tokenizer = AutoTokenizer.from_pretrained(args.model_id, **model_kwargs)

    tokenizer.save_pretrained(export_model_dir)
    print(f" -- [SUCCESS] Tokenizer saved to {export_model_dir}")

    model_kwargs = {
        "trust_remote_code": True,
        # "cache_dir": ".cache",
        "config": AutoConfig.from_pretrained(
            args.model_id,
            trust_remote_code=True,
            #  cache_dir=".cache"
        ),
    }

    if args.quan_type == "int4":
        compression_configs = llm_config.int4_compression_configs
        ov_model = OVModelForCausalLM.from_pretrained(
            args.model_id,
            export=True,
            compile=True,
            quantization_config=OVWeightQuantizationConfig(bits=4, **compression_configs),
            **model_kwargs,
        )
    elif args.quan_type == "int8":
        ov_model = OVModelForCausalLM.from_pretrained(
            args.model_id,
            export=True,
            compile=True,
            load_in_8bit=True,
            **model_kwargs,
        )
    else:
        ov_model = OVModelForCausalLM.from_pretrained(
            args.model_id,
            export=True,
            compile=True,
            load_in_8bit=False,
            **model_kwargs,
        )
    ov_model.save_pretrained(export_model_dir)
    print(f" -- [SUCCESS] model saved to {export_model_dir}")


if __name__ == "__main__":
    main()

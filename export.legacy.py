import argparse
import os

from transformers import AutoTokenizer, AutoConfig
from optimum.intel import OVWeightQuantizationConfig
from optimum.intel.openvino import OVModelForCausalLM


class ExportArgs:

    def get_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--model_id",
            type=str,
            default="THUDM/chatglm3-6b",
            help="The language of the model to use, divided by a : ,such as English:tiny-llama-1b-chat",
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
            default="weights",
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
    model_kwargs = {
        "trust_remote_code": True,
        "config": AutoConfig.from_pretrained(
            args.model_id, trust_remote_code=True
        ),
        "cache_dir": ".cache",
    }
    compression_configs = {
        "sym": False,
        "group_size": 128,
        "ratio": 0.8,
    }

    if args.quan_type == "int4":
        ov_model = OVModelForCausalLM.from_pretrained(
            args.model_id,
            export=True,
            compile=False,
            quantization_config=OVWeightQuantizationConfig(
                bits=4, **compression_configs
            ),
            **model_kwargs
        )
    elif args.quan_type == "int8":
        ov_model = OVModelForCausalLM.from_pretrained(
            args.model_id,
            export=True,
            compile=False,
            load_in_8bit=True,
            **model_kwargs
        )
    else:
        ov_model = OVModelForCausalLM.from_pretrained(
            args.model_id,
            export=True,
            compile=False,
            load_in_8bit=False,
            **model_kwargs
        )
    tokenizer = AutoTokenizer.from_pretrained(
        args.model_id, trust_remote_code=True
    )
    

    ir_model_dir = os.path.join(args.weight_dir, args.model_id+"-ir")
    os.makedirs(ir_model_dir, exist_ok=True)
    tokenizer.save_pretrained(ir_model_dir)

    ov_model.save_pretrained(ir_model_dir)


if __name__ == "__main__":
    main()

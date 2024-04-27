import argparse


class ToyLLMArgs:
    def __init__(self) -> None:
        args = self.get_args()
        self.model_id: str = args.model_id
        self.quan_type: str = args.quan_type
        self.weight_dir: str = args.weight_dir

    def get_args(self):
        parser = argparse.ArgumentParser()
        model_language_name_list = []
        parser.add_argument(
            "--model_id",
            type=str,
            default="THUDM/chatglm3-6b",
            help="The language of the model to use, divided by a : ,such as English:tiny-llama-1b-chat",
        )
        parser.add_argument(
            "--quan_type",
            type=str,
            default="fp16",
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

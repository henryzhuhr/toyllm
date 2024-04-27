from typing import Dict, Union

DEFAULT_SYSTEM_PROMPT = """\
You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.
If a question does not make any sense or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.\
"""

DEFAULT_SYSTEM_PROMPT_CHINESE = """\
你是一个乐于助人、尊重他人以及诚实可靠的助手。\
在安全的情况下，始终尽可能有帮助地回答。\
您的回答不应包含任何有害、不道德、种族主义、性别歧视、有毒、危险或非法的内容。\
请确保您的回答在社会上是公正的和积极的。
如果一个问题没有任何意义或与事实不符，请解释原因，而不是回答错误的问题。如果您不知道问题的答案，请不要分享虚假信息。请尽可能简短的语言回答。\
另外，答案请使用中文。\
"""

DEFAULT_SYSTEM_PROMPT_JAPANESE = """\
あなたは親切で、礼儀正しく、誠実なアシスタントです。 常に安全を保ちながら、できるだけ役立つように答えてください。 回答には、有害、非倫理的、人種差別的、性差別的、有毒、危険、または違法なコンテンツを含めてはいけません。 回答は社会的に偏見がなく、本質的に前向きなものであることを確認してください。
質問が意味をなさない場合、または事実に一貫性がない場合は、正しくないことに答えるのではなく、その理由を説明してください。 質問の答えがわからない場合は、誤った情報を共有しないでください。\
"""

DEFAULT_RAG_PROMPT = """\
You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.\
"""

DEFAULT_RAG_PROMPT_CHINESE = """\
基于以下已知信息，请简洁并专业地回答用户的问题。如果无法从中得到答案，请说 "根据已知信息无法回答该问题" 或 "没有提供足够的相关信息"。不允许在答案中添加编造成分。另外，答案请使用中文。\
"""


class SupportedLLMConfig:
    def __init__(
        self,
        language: str = "English",
        model_id: str = "THUDM/chatglm3-6b",
        int4_compression_configs: Dict[str, Union[bool, float, int]] = {
            "sym": False,
            "group_size": 128,
            "ratio": 0.8,
        },
        tokenizer_kwargs: Dict = {},
        model_kwargs: Dict = {},
    ) -> None:
        self.language = language
        self.model_id = model_id
        self.int4_compression_configs = int4_compression_configs
        self.tokenizer_kwargs = tokenizer_kwargs
        self.model_kwargs = model_kwargs


SUPPORTED_LLM_LIST = [
    SupportedLLMConfig(
        "English",
        "THUDM/chatglm3-6b",
        int4_compression_configs={
            "sym": True,
            "group_size": 128,
            "ratio": 0.72,
        },
        tokenizer_kwargs={"add_special_tokens": False},
    ),
    SupportedLLMConfig(
        "Chinese",
        "Qwen/Qwen1.5-1.8B-Chat",
        tokenizer_kwargs={"add_special_tokens": False},
        model_kwargs={
            "start_message": DEFAULT_SYSTEM_PROMPT_CHINESE,
            "stop_tokens": ["<|im_end|>", "<|endoftext|>"],
        },
    ),
]

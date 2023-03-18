from typing import Dict, List

import tiktoken

from ..config import TurboModel

__all__ = [
    "count_tokens",
    "get_max_tokens_length",
]

# See: https://platform.openai.com/docs/models/gpt-4
MODEL_WINDOWS: Dict[str, int] = {
    "gpt-4": 8_192,
    "gpt-4-32k": 32_768,
    "gpt-3.5-turbo": 4_096,
    "text-davinci": 4_097,
    "text-curie": 2_049,
    "text-babbage": 2_049,
    "text-ada": 2_049,
    "code-davinci": 8_001,
    "code-cushman": 2_048,
    "davinci": 2_049,
    "curie": 2_049,
    "babbage": 2_049,
    "ada": 2_049,
}


def get_max_tokens_length(model_name: str) -> int:
    for model_prefix, window in MODEL_WINDOWS.items():
        if model_name.startswith(model_prefix):
            return window

    raise ValueError(f"{model_name} is not a known openai model")


def count_tokens(messages: List[dict], model: TurboModel) -> int:
    """Count the number of tokens stored in list of messages."""

    # Get tiktoken encoding
    encoding = tiktoken.encoding_for_model(model)

    ###########
    # From https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb  # noqa: E501
    ###########
    if model == "gpt-3.5-turbo-0301":  # note: future models may deviate from this
        num_tokens = 0
        for message in messages:
            # every message follows <im_start>{role/name}\n{content}<im_end>\n
            num_tokens += 4
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":  # if there's a name, the role is omitted
                    num_tokens += -1  # role is always required and always 1 token
        num_tokens += 2  # every reply is primed with <im_start>assistant
        return num_tokens
    ###########

    # Else, just sum up
    texts: List[str] = [message["content"] for message in messages]
    tokens_list: List[List[int]] = [encoding.encode(text) for text in texts]

    count: int = 2 + sum([len(tokens) + 4 for tokens in tokens_list])

    return count

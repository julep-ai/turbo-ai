from typing import (
    Callable,
    List,
    Optional,
)

import openai
from openai.openai_object import OpenAIObject


from .structs import Assistant
from .types import (
    BaseCache,
    BaseMemory,
)


from .utils import with_retries

__all__ = [
    "run_chat",
]


# Chat runner
@with_retries
async def run_chat(
    memory: BaseMemory,
    cache: Optional[BaseCache] = None,
    select_choice: Callable[[List[OpenAIObject]], OpenAIObject] = (
        lambda choices: choices[0]
    ),
    **kwargs,
) -> Assistant:
    """Run ChatCompletion for the memory so far"""

    # Get messages from memory
    max_tokens = kwargs.get("max_tokens")
    prompt = await memory.prepare_prompt(max_tokens=max_tokens)

    # Check cache
    if cache and await cache.has(prompt):
        cached = await cache.get(prompt)

        result = Assistant(**cached)
        await memory.append(result)

        return result

    # Create completion
    chat_completion = await openai.ChatCompletion.acreate(
        messages=prompt,
        **kwargs,
    )

    # Parse result
    output = select_choice(chat_completion.choices).message
    payload = dict(content=output["content"])
    result = Assistant(**payload)

    # Append result to memory
    await memory.append(result)

    # Add to cache
    if cache:
        await cache.set(prompt, payload)

    return result

from typing import (
    Optional,
)

import openai


from .types import (
    Assistant,
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
    **kwargs,
) -> Assistant:
    """Run ChatCompletion for the memory so far"""

    # Get messages from memory
    messages = await memory.get_dicts()
    if cache and await cache.has(messages):
        cached = await cache.get(messages)
        return Assistant(**cached)

    # Create completion
    chat_completion = await openai.ChatCompletion.acreate(
        messages=messages,
        **kwargs,
    )

    # Parse result
    output = chat_completion.choices[0].message
    payload = dict(content=output["content"])
    result = Assistant(**payload)

    # Append result to memory
    await memory.append(result)

    # Add to cache
    if cache:
        await cache.set(messages, payload)

    return result

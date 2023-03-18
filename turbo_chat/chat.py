from typing import (
    Optional,
)

import openai


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
    **kwargs,
) -> Assistant:
    """Run ChatCompletion for the memory so far"""

    # Get messages from memory
    max_tokens = kwargs.get("max_tokens")
    prompt = await memory.prepare_prompt(max_tokens=max_tokens)

    # Check cache
    if cache and await cache.has(prompt):
        cached = await cache.get(prompt)
        return Assistant(**cached)

    # Create completion
    chat_completion = await openai.ChatCompletion.acreate(
        messages=prompt,
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
        await cache.set(prompt, payload)

    return result

from typing import Awaitable, Callable

__all__ = [
    "Tool",
]

Tool = Callable[..., Awaitable[str]]

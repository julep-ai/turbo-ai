from typing import Awaitable, Callable, Optional, TypedDict

__all__ = [
    "Tool",
    "ToolBotInput",
]

Tool = Callable[..., Awaitable[str]]


class ToolBotInput(TypedDict):
    state: Optional[str]
    input: str

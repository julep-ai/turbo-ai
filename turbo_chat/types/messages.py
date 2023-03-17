from abc import ABC, abstractmethod
from typing import (
    cast,
    List,
    Literal,
    TypedDict,
)

import pydantic


__all__ = [
    "MessageRole",
    "PrefixMessage",
    "MessageDict",
    "BasePrefixMessageCollection",
]


# Enums
# Allowed values for openai chatml prefixes
MessageRole = Literal[
    "system",
    "user",
    "assistant",
    "system name=example_user",
    "system name=example_assistant",
]


# Models
class PrefixMessage(pydantic.BaseModel):
    """Container for a single chatml prefix message"""

    role: MessageRole
    content: str
    forward: bool = False


class MessageDict(TypedDict):
    role: MessageRole
    content: str


# Abstract classes
class BasePrefixMessageCollection(ABC):
    """Base class for async collections of prefix messages"""

    @abstractmethod
    async def get(self) -> List[PrefixMessage]:
        ...

    async def get_dicts(self) -> List[MessageDict]:
        messages = await self.get()

        return [
            cast(MessageDict, message.dict(include={"role", "content"}))
            for message in messages
        ]

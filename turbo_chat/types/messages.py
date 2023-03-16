from abc import ABC, abstractmethod
from typing import (
    Dict,
    List,
    Literal,
)

import pydantic


__all__ = [
    "System",
    "User",
    "Assistant",
    "ExampleUser",
    "ExampleAssistant",
    "MessageRole",
    "PrefixMessage",
    "BasePrefixMessageCollection",
    "Example",
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
    yield_downstream: bool = False


class System(PrefixMessage):
    """System message"""

    role: MessageRole = "system"


class User(PrefixMessage):
    """User message"""

    role: MessageRole = "user"


class Assistant(PrefixMessage):
    """Assistant message"""

    role: MessageRole = "assistant"
    yield_downstream: bool = True


class ExampleUser(PrefixMessage):
    """User example message"""

    role: MessageRole = "system name=example_user"


class ExampleAssistant(PrefixMessage):
    """Assistant example message"""

    role: MessageRole = "system name=example_assistant"


# Abstract classes
class BasePrefixMessageCollection(ABC):
    """Base class for async collections of prefix messages"""

    @abstractmethod
    async def get(self) -> List[PrefixMessage]:
        ...

    async def get_dicts(self) -> List[Dict[str, str]]:
        messages = await self.get()
        return [message.dict(include={"role", "content"}) for message in messages]


# Abstract implementations
class Example(BasePrefixMessageCollection, pydantic.BaseModel):
    user: str
    assistant: str

    async def get(self) -> List[PrefixMessage]:
        return [
            ExampleUser(content=self.user),
            ExampleAssistant(content=self.assistant),
        ]

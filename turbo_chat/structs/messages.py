from typing import (
    List,
)

import pydantic

from ..types.messages import (
    BasePrefixMessageCollection,
    MessageRole,
    PrefixMessage,
)


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


# Models
class System(PrefixMessage):
    """System message"""

    role: MessageRole = "system"


class User(PrefixMessage):
    """User message"""

    role: MessageRole = "user"


class Assistant(PrefixMessage):
    """Assistant message"""

    role: MessageRole = "assistant"
    forward: bool = True


class ExampleUser(PrefixMessage):
    """User example message"""

    role: MessageRole = "system name=example_user"


class ExampleAssistant(PrefixMessage):
    """Assistant example message"""

    role: MessageRole = "system name=example_assistant"


# Abstract implementations
class Example(BasePrefixMessageCollection, pydantic.BaseModel):
    user: str
    assistant: str

    async def get(self) -> List[PrefixMessage]:
        return [
            ExampleUser(content=self.user),
            ExampleAssistant(content=self.assistant),
        ]

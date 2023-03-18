from typing import (
    List,
)

import pydantic

from ..types.messages import (
    BaseMessageCollection,
    MessageRole,
    Message,
)


__all__ = [
    "System",
    "User",
    "Assistant",
    "ExampleUser",
    "ExampleAssistant",
    "MessageRole",
    "Message",
    "BaseMessageCollection",
    "Example",
]


# Models
class System(Message):
    """System message"""

    role: MessageRole = "system"


class User(Message):
    """User message"""

    role: MessageRole = "user"


class Assistant(Message):
    """Assistant message"""

    role: MessageRole = "assistant"
    forward: bool = True


class ExampleUser(Message):
    """User example message"""

    role: MessageRole = "system name=example_user"


class ExampleAssistant(Message):
    """Assistant example message"""

    role: MessageRole = "system name=example_assistant"


# Abstract implementations
class Example(BaseMessageCollection, pydantic.BaseModel):
    user: str
    assistant: str

    async def get(self) -> List[Message]:
        return [
            ExampleUser(content=self.user),
            ExampleAssistant(content=self.assistant),
        ]

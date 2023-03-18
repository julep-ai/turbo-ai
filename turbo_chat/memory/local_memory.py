from typing import (
    List,
)

import pydantic


from ..types.memory import BaseMemory
from ..types.messages import Message

__all__ = [
    "LocalMemory",
]


# Abstract implementations
class LocalMemory(BaseMemory, pydantic.BaseModel):
    """Store messages in an in-memory list"""

    state: dict = {}
    messages: List[Message] = []

    async def get(self) -> List[Message]:
        return [
            message for message in self.messages if isinstance(message, Message)
        ]

    async def append(self, item) -> None:
        self.messages.append(item)

    async def clear(self) -> None:
        self.messages = []

    async def get_state(self) -> dict:
        return self.state

    async def set_state(self, new_state: dict, merge: bool = False) -> None:
        self.state = (
            new_state
            if not merge
            else {
                **self.state,
                **new_state,
            }
        )

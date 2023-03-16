from typing import (
    List,
)

import pydantic


from ..types.memory import BaseMemory
from ..types.messages import PrefixMessage

__all__ = [
    "ListMemory",
]


# Abstract implementations
class ListMemory(BaseMemory, pydantic.BaseModel):
    """Store messages in an in-memory list"""

    messages: List[PrefixMessage] = []

    async def get(self) -> List[PrefixMessage]:
        return [
            message for message in self.messages if isinstance(message, PrefixMessage)
        ]

    async def append(self, item) -> None:
        self.messages.append(item)

    async def clear(self) -> None:
        self.messages = []

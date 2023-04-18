from typing import List

from ..types.memory import BaseMemory
from ..types.messages import Message

__all__ = [
    "LocalMemory",
]


# Abstract implementations
class LocalMemory(BaseMemory):
    """Store messages in an in-memory list"""

    state: dict = {}
    messages: List[Message] = []

    async def get(self) -> List[Message]:
        return [message for message in self.messages]

    async def extend(self, items) -> None:
        self.messages.extend(items)

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

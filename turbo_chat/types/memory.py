from abc import abstractmethod
from typing import List, Optional

import pydantic

from ..config import TurboModel
from .messages import (
    BaseMessageCollection,
    MessageDict,
    Message,
)

__all__ = [
    "BaseMemory",
]


# Abstract classes
class BaseMemory(BaseMessageCollection, pydantic.BaseModel):
    """Base class for persisting conversation history and state."""

    model: TurboModel

    async def init(self, context={}) -> None:
        ...

    @abstractmethod
    async def extend(self, items: List[Message]) -> None:
        ...

    @abstractmethod
    async def get_state(self) -> dict:
        ...

    @abstractmethod
    async def set_state(self, new_state: dict, merge: bool = False) -> None:
        ...

    async def append(self, item: Message) -> None:
        await self.extend([item])

    async def prepare_prompt(
        self,
        max_tokens: Optional[int] = None,
    ) -> List[MessageDict]:
        """Turn message history into a prompt for openai."""

        # Noop: Override to add filtering
        messages: List[MessageDict] = await self.get_dicts()
        return messages

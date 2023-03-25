from abc import abstractmethod
from typing import List

import pydantic

from ..config import TurboModel
from .messages import (
    BaseMessageCollection,
    MessageDict,
    Message,
)

from .misc import WithSetup


__all__ = [
    "BaseMemory",
]


# Abstract classes
class BaseMemory(BaseMessageCollection, WithSetup, pydantic.BaseModel):
    """Base class for persisting conversation history and state."""

    model: TurboModel

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
        max_tokens: int = 0,
    ) -> List[MessageDict]:
        """Turn message history into a prompt for openai."""

        # Noop: Override to add filtering
        messages: List[MessageDict] = await self.get_dicts()
        return messages

import tiktoken
from abc import abstractmethod
from typing import (
    List,
)


from .messages import BasePrefixMessageCollection, PrefixMessage
from ..types import TurboModel

__all__ = [
    "BaseMemory",
]


# Abstract classes
class BaseMemory(BasePrefixMessageCollection):
    """Base class for interface for persisting prefix messages for a session"""

    model_name: TurboModel

    async def init(self, model_name: TurboModel, context={}) -> None:
        self.model_name = model_name

    @abstractmethod
    async def append(self, item: PrefixMessage) -> None:
        ...

    @abstractmethod
    async def clear(self) -> None:
        ...

    async def extend(self, items: List[PrefixMessage]) -> None:
        for item in items:
            await self.append(item)

    async def count(self) -> int:
        encoding = tiktoken.encoding_for_model(self.model_name)
        count = 0
        for dict_ in await self.get_dicts():
            for v in dict_.values():
                count += len(encoding.encode(v))

        return count

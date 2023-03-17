from abc import abstractmethod
from typing import (
    List,
)


from .messages import BasePrefixMessageCollection, PrefixMessage

__all__ = [
    "BaseMemory",
]


# Abstract classes
class BaseMemory(BasePrefixMessageCollection):
    """Base class for interface for persisting prefix messages for a session"""

    async def init(self, context={}) -> None:
        ...

    @abstractmethod
    async def append(self, item: PrefixMessage) -> None:
        ...

    @abstractmethod
    async def clear(self) -> None:
        ...

    async def extend(self, items: List[PrefixMessage]) -> None:
        for item in items:
            await self.append(item)

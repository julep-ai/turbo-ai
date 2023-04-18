from abc import ABC, abstractmethod
import json
from typing import (
    Any,
)

from .misc import WithSetup


__all__ = [
    "BaseCache",
]


# Abstract classes
class BaseCache(ABC, WithSetup):
    """Base class for caching agent responses"""

    def serialize(self, obj: Any) -> Any:
        return obj

    def deserialize(self, hashed: Any) -> Any:
        return hashed

    def to_key(self, obj: Any) -> str:
        return json.dumps(self.serialize(obj))

    @abstractmethod
    async def has(self, key: Any) -> bool:
        ...

    @abstractmethod
    async def set(self, key: Any, value: Any) -> None:
        ...

    @abstractmethod
    async def get(self, key: Any) -> Any:
        ...

    @abstractmethod
    async def clear(self) -> Any:
        ...

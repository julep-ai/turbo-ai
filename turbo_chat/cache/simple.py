from typing import (
    Any,
)

import pydantic


from ..types.cache import BaseCache

__all__ = [
    "SimpleCache",
]


class SimpleCache(BaseCache, pydantic.BaseModel):
    """Simple in-memory cache"""

    cache: dict = {}

    async def has(self, key) -> bool:
        return self.to_key(key) in self.cache

    async def set(self, key, value) -> None:
        self.cache[self.to_key(key)] = self.serialize(value)

    async def get(self, key) -> Any:
        assert await self.has(key), "No cache entry found"
        return self.deserialize(self.cache[self.to_key(key)])

    async def clear(self) -> Any:
        self.cache = {}

import asyncio
import json
from typing import Any

import redis.asyncio as redis

from ..types.cache import BaseCache

__all__ = [
    "RedisCache",
]


class RedisCache(BaseCache):
    """Redis cache"""

    client: redis.Redis
    prefix: str

    async def setup(
        self,
        client: redis.Redis,
        prefix: str = "turbo_cache",
    ):
        self.client = client
        self.prefix = prefix

    def serialize(self, obj: Any) -> str:
        return json.dumps(obj)

    def deserialize(self, hashed: str) -> Any:
        return json.loads(hashed)

    def to_key(self, key) -> str:
        return f"{self.prefix}:{super().to_key(key)}"

    async def has(self, key) -> bool:
        result: int = await self.client.exists(self.to_key(key))
        return bool(result)

    async def set(self, key, value) -> None:
        _key = self.to_key(key)
        _value = self.serialize(value)

        await self.client.set(_key, _value)

    async def get(self, key) -> Any:
        _key = self.to_key(key)
        result = await self.client.get(_key)

        assert result, "key not found"

        return self.deserialize(result)

    async def clear(self) -> None:
        keys = [key async for key in self.client.scan_iter(f"{self.prefix}:*")]
        await asyncio.gather(*map(self.client.delete, keys))

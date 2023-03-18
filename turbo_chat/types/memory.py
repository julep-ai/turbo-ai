from abc import abstractmethod
from typing import List, Optional

import pydantic
from tiktoken.core import Encoding

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
    """Base class for interface for persisting prefix messages for a session"""

    class Config:
        # Needed because no validator for Encoding
        arbitrary_types_allowed = True

    encoding: Optional[Encoding] = None

    async def init(self, context={}) -> None:
        ...

    @abstractmethod
    async def append(self, item: Message) -> None:
        ...

    @abstractmethod
    async def clear(self) -> None:
        ...

    async def get_state(self) -> dict:
        raise NotImplementedError()

    async def set_state(self, new_state: dict, merge: bool = False) -> None:
        raise NotImplementedError()

    async def extend(self, items: List[Message]) -> None:
        for item in items:
            await self.append(item)

    async def count_tokens(self) -> int:
        """Count the number of tokens stored in the memory."""

        assert self.encoding, "tiktoken.Encoding is required"

        messages: List[MessageDict] = await self.get_dicts()
        texts: List[str] = [message["content"] for message in messages]
        tokens_list: List[List[int]] = [self.encoding.encode(text) for text in texts]

        count: int = sum([len(tokens) for tokens in tokens_list])

        return count

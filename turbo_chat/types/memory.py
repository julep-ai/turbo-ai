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
    """Base class for persisting conversation history and state."""

    class Config:
        # Needed because no validator for Encoding
        arbitrary_types_allowed = True

    encoding: Optional[Encoding] = None

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

    async def prepare_prompt(self) -> List[MessageDict]:
        """Turn message history into a prompt for openai."""

        # Noop: Override to add filtering
        messages: List[MessageDict] = await self.get_dicts()
        return messages

    async def count_tokens(self) -> int:
        """Count the number of tokens stored in the memory."""

        assert self.encoding, "tiktoken.Encoding is required for counting tokens"

        messages: List[MessageDict] = await self.prepare_prompt()
        texts: List[str] = [message["content"] for message in messages]
        tokens_list: List[List[int]] = [self.encoding.encode(text) for text in texts]

        count: int = sum([len(tokens) for tokens in tokens_list])

        return count

from abc import abstractmethod
from itertools import groupby
from operator import attrgetter
from typing import cast, List

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

        messages = await self.get()
        messages = sorted(messages, key=attrgetter("label", "timestamp"))

        sticky_top, sticky_bottom, non_sticky = (
            [
                message
                for message in messages
                if message.sticky and message.sticky_position == "top"
            ],
            [
                message
                for message in messages
                if message.sticky and message.sticky_position == "bottom"
            ],
            [message for message in messages if not message.sticky],
        )

        # Take only last for every label group
        sticky_top = [
            list(group)[-1] for _, group in groupby(sticky_top, key=attrgetter("label"))
        ]

        sticky_bottom = [
            list(group)[-1]
            for _, group in groupby(sticky_bottom, key=attrgetter("label"))
        ]

        if len(non_sticky):
            *head, last = non_sticky
            append = [last]
        else:
            head = []
            append = []

        messages = sticky_top + head + sticky_bottom + append

        # Convert
        message_dicts = [cast(MessageDict, message.dict()) for message in messages]

        # Add prefix (system name=) for examples
        for i, message in enumerate(message_dicts):
            if message["role"].startswith("example"):
                message_dicts[i]["role"] = f"system name={message['role']}"

        # max_tokens will be used by extending classes

        return message_dicts

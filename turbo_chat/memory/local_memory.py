from typing import List

import pydantic


from ..types.memory import BaseMemory
from ..types.messages import Message, MessageDict
from ..utils import count_tokens, get_max_tokens_length

__all__ = [
    "LocalMemory",
]


# Abstract implementations
class LocalMemory(BaseMemory, pydantic.BaseModel):
    """Store messages in an in-memory list"""

    state: dict = {}
    messages: List[Message] = []

    async def get(self) -> List[Message]:
        return [message for message in self.messages]

    async def extend(self, items) -> None:
        self.messages.extend(items)

    async def get_state(self) -> dict:
        return self.state

    async def set_state(self, new_state: dict, merge: bool = False) -> None:
        self.state = (
            new_state
            if not merge
            else {
                **self.state,
                **new_state,
            }
        )

    async def prepare_prompt(
        self,
        max_tokens: int = 0,
    ) -> List[MessageDict]:
        """Drop messages iteratively to keep max_tokens + length < context_window."""
        """Keep first and last message."""

        max_tokens = max_tokens or 0
        context_window: int = get_max_tokens_length(self.model) - max_tokens
        messages = await super().prepare_prompt()

        # Make sure first message is within limits
        first, *rest = messages
        assert count_tokens([first], self.model) <= context_window

        if not len(rest):
            return messages

        # Make sure first and last combined are also within limits
        *middle, last = rest
        total = count_tokens([first, last], self.model)
        assert total <= context_window

        # Iteratively filter middle (remove from end)
        final = [first]

        while (
            len(middle)
            and (total := total + count_tokens(middle[-1:], self.model))
            <= context_window
        ):
            final.insert(1, middle.pop())

        return final

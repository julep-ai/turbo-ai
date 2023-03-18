from typing import List


from ..config import TurboModel
from ..types.messages import MessageDict
from ..utils import count_tokens, get_max_tokens_length
from .local_memory import LocalMemory

__all__ = [
    "LocalTruncatedMemory",
    "MemoryTruncation",
]


# Abstract implementations
class MemoryTruncation:
    """Mixin for automatic truncation"""

    model: TurboModel

    async def prepare_prompt(
        self,
        max_tokens: int = 0,
    ) -> List[MessageDict]:
        """Drop messages iteratively to keep max_tokens + length < context_window."""
        """Keep first and last message."""

        max_tokens = max_tokens or 0
        context_window: int = get_max_tokens_length(self.model) - max_tokens
        messages = await super().prepare_prompt()  # type: ignore

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


class LocalTruncatedMemory(MemoryTruncation, LocalMemory):
    """Local memory with automatic truncation"""

    ...

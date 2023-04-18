from typing import List


from ..structs import User
from ..types.messages import MessageDict
from .local_memory import LocalMemory
from .truncated_memory import MemoryTruncation

__all__ = [
    "LocalSummarizeMemory",
    "MemorySummarization",
]


# Abstract implementations
class MemorySummarization(MemoryTruncation):
    """Mixin for automatic summarization"""

    async def prepare_prompt(
        self,
        max_tokens: int = 0,
    ) -> List[MessageDict]:
        """Summarize the conversation."""

        # To avoid circular imports
        from ..bots import summarize_bot

        # Get first, middle, last message
        messages = await super().prepare_prompt()  # type: ignore
        first, *rest = messages
        if not len(rest):
            return messages

        *middle, last = rest
        if not len(middle):
            return messages

        # Summarize the middle conversation
        conversation = "\n".join(
            [f"{message['role']}: {message['content']}" for message in messages]
        )

        summary = await summarize_bot(text=conversation, text_type="conversation").run()

        summary_as_user = User(summary.content).dict()

        return [first, summary_as_user, last]


class LocalSummarizeMemory(MemorySummarization, LocalMemory):
    """Local memory with automatic summarization"""

    ...

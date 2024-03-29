from typing import Any, Optional, Protocol

import pydantic

from .signals import GetInput

__all__ = [
    "Result",
]


class HasContent(Protocol):
    content: str


class Result(pydantic.BaseModel):
    """Holds the result yielded by a turbo app."""

    content: Any
    needs_input: bool = False
    done: bool = False
    original_role: Optional[str] = None

    @classmethod
    def from_message(
        cls,
        message: HasContent,
        done: bool = False,
    ) -> "Result":
        assert hasattr(message, "content"), "Content holder object required"
        role = getattr(message, "role", None)

        return cls(
            content=message.content,
            original_role=role,
            needs_input=isinstance(message, GetInput),
            done=done,
        )

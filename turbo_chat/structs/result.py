from typing import Protocol, Optional, Union

import pydantic

from .signals import GetInput

__all__ = [
    "Result",
]


class HasContent(Protocol):
    content: Union[str, dict]


class Result(pydantic.BaseModel):
    """Holds the result yielded by a turbo app."""

    content: Optional[Union[str, dict]]
    needs_input: bool = False
    done: bool = False

    @classmethod
    def from_message(
        cls,
        message: HasContent,
        done: bool = False,
    ) -> "Result":
        assert hasattr(message, "content"), "Content holder object required"

        return cls(
            content=message.content,
            needs_input=isinstance(message, GetInput),
            done=done,
        )

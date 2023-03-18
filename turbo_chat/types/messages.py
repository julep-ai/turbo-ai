from abc import ABC, abstractmethod
from typing import (
    cast,
    List,
    Literal,
    Optional,
    TypedDict,
)

import pydantic

from ..utils import render_template

__all__ = [
    "MessageRole",
    "Message",
    "MessageDict",
    "BaseMessageCollection",
]


# Enums
# Allowed values for openai chatml prefixes
MessageRole = Literal[
    "system",
    "user",
    "assistant",
    "system name=example_user",
    "system name=example_assistant",
]


# Models
class Message(pydantic.BaseModel):
    """Container for a single chatml prefix message"""

    role: MessageRole

    # Content / Template
    content: Optional[str] = None
    template: Optional[str] = None
    variables: Optional[dict] = None

    # Check template variables
    check: bool = False

    # Should forward downstream
    forward: bool = False

    @pydantic.root_validator
    def validate_content_template(cls, values: dict) -> dict:
        # Get vals
        content = values["content"]
        check = values["check"]
        template_string = values.pop("template")
        variables = values.pop("variables")

        # Check that correct values set
        template_set = bool(template_string) and (variables is not None)
        assert template_set ^ (
            content is not None
        ), "Either content or template/variables must be set"

        # Render template
        if template_set:
            values["content"] = render_template(template_string, variables, check)

        return values


class MessageDict(TypedDict):
    role: MessageRole
    content: str


# Abstract classes
class BaseMessageCollection(ABC):
    """Base class for async collections of prefix messages"""

    @abstractmethod
    async def get(self) -> List[Message]:
        ...

    async def get_dicts(self) -> List[MessageDict]:
        messages = await self.get()

        return [
            cast(MessageDict, message.dict(include={"role", "content"}))
            for message in messages
        ]

from abc import ABC, abstractmethod
from datetime import datetime
import json
from typing import (
    cast,
    List,
    Literal,
    Optional,
    TypedDict,
    Union,
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
    "example_user",  # Will add prefix (system name=) in prepare_prompt
    "example_assistant",
]


# Models
class MessageDict(TypedDict):
    role: str
    content: str


class Message(pydantic.BaseModel):
    """Container for a single chatml prefix message"""

    role: MessageRole
    timestamp: datetime = pydantic.Field(default_factory=datetime.utcnow)

    # Content / Template
    content: Optional[Union[str, dict]] = None
    template: Optional[str] = None
    variables: Optional[dict] = None

    # Check template variables
    check: bool = False

    # Stickiness
    sticky: bool = False
    label: str = ""
    sticky_position: Literal["top", "bottom"] = "bottom"

    # Should forward downstream
    forward: bool = False

    @pydantic.root_validator
    def validate_content_template(cls, values: dict) -> dict:
        # Get vals
        content = values["content"]
        check = values["check"]
        template_string = values.pop("template")
        variables = values.pop("variables")
        sticky = values["sticky"]
        label = values["label"]
        role = values["role"]

        # Label can be system only if role is system
        if label == "system":
            assert role == "system", "System label can only be used with system role"

        # Check that sticky messages have an id
        assert not (sticky ^ bool(label)), "Sticky must be set with label"

        # Check that correct values set
        template_set = bool(template_string) and (variables is not None)
        assert template_set ^ (
            content is not None
        ), "Either content or template/variables must be set"

        # Render template
        if template_set:
            values["content"] = render_template(template_string, variables, check)

        return values

    def dict(self, **kwargs) -> MessageDict:
        # Include role and content
        kwargs.setdefault("include", {"role", "content"})
        data = super().dict(**kwargs)

        # Convert content to json if not str
        if not isinstance(data["content"], str):
            data["content"] = json.dumps(data["content"])

        return cast(MessageDict, data)


# Abstract classes
class BaseMessageCollection(ABC):
    """Base class for async collections of prefix messages"""

    @abstractmethod
    async def get(self) -> List[Message]:
        ...

    async def get_dicts(self) -> List[MessageDict]:
        messages = await self.get()

        # Convert
        message_dicts = [cast(MessageDict, message.dict()) for message in messages]

        return message_dicts

from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from functools import cached_property
import json
from typing import (
    List,
    Optional,
    Union,
)

import pydantic

from ..utils import render_template

__all__ = [
    "MessageRole",
    "Message",
    "ChatMLMessage",
]


# Enums
# Allowed values for openai chatml prefixes
class MessageRole(str, Enum):
    System = "system"
    User = "user"
    Assistant = "assistant"


# Models
class ChatMLMessage(
    pydantic.BaseModel,
    extra=pydantic.Extra.forbid,
    frozen=True,
    use_enum_values=True,
):
    role: MessageRole
    content: str


class Message(
    pydantic.BaseModel,
    extra=pydantic.Extra.ignore,
    use_enum_values=True,
):
    """Container for a single chatml prefix message"""

    role: MessageRole
    timestamp: datetime = pydantic.Field(default_factory=datetime.utcnow)
    metadata: dict = pydantic.Field(default_factory=dict)

    # Content / Template
    content: Optional[Union[str, dict]] = None
    template: Optional[str] = None
    variables: Optional[dict] = None

    # Check template variables
    check: bool = False

    def dict(self, **kwargs) -> dict:
        # Exclude config values by default
        kwargs.setdefault("exclude", {"template", "variables", "check"})
        return super().dict(**kwargs)


    def to_chatml(self) -> ChatMLMessage:
        """Convert to chatml message"""

        keys = ChatMLMessage.schema()["properties"].keys()
        data = self.dict(include=set(keys))

        # Convert content to json if not str
        if not isinstance(data["content"], str):
            data["content"] = json.dumps(data["content"])

        return ChatMLMessage(**data)


    @pydantic.root_validator
    def validate_content_template(cls, values: dict) -> dict:
        # Get vals
        content = values["content"]
        check = values["check"]
        template_string = values.pop("template")
        variables = values.pop("variables")
        role = values["role"]

        # Check that correct values set
        template_set = bool(template_string) and (variables is not None)
        assert template_set ^ (
            content is not None
        ), "Either content or template/variables must be set"

        # Render template
        if template_set:
            values["content"] = render_template(template_string, variables, check)

        return values


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

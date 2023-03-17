from abc import ABC, abstractmethod
from typing import (
    cast,
    List,
    Literal,
    Optional,
    TypedDict,
)

from jinja2 import Environment
import pydantic


__all__ = [
    "MessageRole",
    "PrefixMessage",
    "MessageDict",
    "BasePrefixMessageCollection",
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


# Utils
jinja_env: Environment = Environment(
    autoescape=False,
    trim_blocks=True,
    lstrip_blocks=True,
)


# Models
class PrefixMessage(pydantic.BaseModel):
    """Container for a single chatml prefix message"""

    role: MessageRole

    content: Optional[str] = None
    template: Optional[str] = None
    variables: Optional[dict] = None

    forward: bool = False

    @pydantic.root_validator
    def validate_content_template(cls, values: dict) -> dict:
        content = values["content"]
        template_string = values.pop("template")
        variables = values.pop("variables")

        template_set = bool(template_string) and bool(variables)
        assert template_set ^ bool(
            content
        ), "Either content or template/variables must be set"

        # Render template
        if template_set:
            template = jinja_env.from_string(template_string)
            values["content"] = template.render(**variables)

        return values


class MessageDict(TypedDict):
    role: MessageRole
    content: str


# Abstract classes
class BasePrefixMessageCollection(ABC):
    """Base class for async collections of prefix messages"""

    @abstractmethod
    async def get(self) -> List[PrefixMessage]:
        ...

    async def get_dicts(self) -> List[MessageDict]:
        messages = await self.get()

        return [
            cast(MessageDict, message.dict(include={"role", "content"}))
            for message in messages
        ]

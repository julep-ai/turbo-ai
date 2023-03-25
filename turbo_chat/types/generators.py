from typing import (
    Any,
    AsyncGenerator,
    Optional,
    Protocol,
    Union,
)


from ..structs.proxies import TurboGenWrapper
from ..structs.result import Result
from ..structs.signals import Generate, GetInput

from .messages import Message
from .memory import BaseMemory

__all__ = [
    "TurboGenWrapper",
]


# Types
TurboGenTemplate = AsyncGenerator[
    Union[Message, Generate, GetInput, Result],
    Any,
]


class TurboGenTemplateFn(Protocol):
    def __call__(
        self,
        memory: Optional[BaseMemory] = None,
        **context,
    ) -> TurboGenTemplate:
        ...


class TurboGenFn(Protocol):
    fn: TurboGenTemplateFn
    settings: dict

    def configure(self, new_settings: dict) -> "TurboGenFn":
        ...

    def __call__(
        self,
        **context,
    ) -> TurboGenWrapper:
        ...

from typing import (
    Any,
    AsyncGenerator,
    Optional,
    Protocol,
    Union,
)


from ..structs.result import Result
from ..structs.signals import Generate, GetInput

from .messages import PrefixMessage
from .memory import BaseMemory

__all__ = [
    "TurboGen",
]


# Types
TurboGen = AsyncGenerator[Result, Any]
TurboGenTemplate = AsyncGenerator[
    Union[PrefixMessage, Generate, GetInput],
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
    ) -> TurboGen:
        ...

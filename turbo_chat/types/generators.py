from typing import (
    Any,
    AsyncGenerator,
    Optional,
    Protocol,
    Union,
)


from ..structs.messages import Assistant
from ..structs.signals import GetInput

from .messages import PrefixMessage
from .memory import BaseMemory

__all__ = [
    "TurboGen",
]


# Types
TurboGen = AsyncGenerator[Union[Assistant, GetInput], Any]
TurboGenTemplate = AsyncGenerator[PrefixMessage, Any]


class TurboGenTemplateFn(Protocol):
    def __call__(
        self,
        memory: Optional[BaseMemory] = None,
        **context,
    ) -> TurboGenTemplate:
        ...


class TurboGenFn(Protocol):
    fn: TurboGenTemplateFn

    def __call__(
        self,
        **context,
    ) -> TurboGen:
        ...

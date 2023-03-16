from typing import (
    Any,
    AsyncGenerator,
    Optional,
    Protocol,
    Union,
)


from .messages import Assistant, PrefixMessage
from .memory import BaseMemory
from .signals import GetUserInput

__all__ = [
    "TurboGen",
]


# Types
TurboGen = AsyncGenerator[Union[Assistant, GetUserInput], Any]
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

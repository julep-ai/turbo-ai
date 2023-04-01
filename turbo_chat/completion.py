from typing import (
    Awaitable,
    Callable,
    Protocol,
    Union,
)


from .structs import (
    Generate,
    User,
)

from .turbo import turbo

from .utils.args import ensure_args


__all__ = [
    "completion",
]


class CompletionFnWithResult(Protocol):
    def __call__(self, result: str, **kwargs) -> Awaitable[str]:
        ...


class CompletionFnWithoutResult(Protocol):
    def __call__(self, **kwargs) -> Awaitable[None]:
        ...


CompletionFn = Union[CompletionFnWithResult, CompletionFnWithoutResult]


class Completion(Protocol):
    def __call__(self, **kwargs) -> Awaitable[str]:
        ...


# Decorator
def completion(**opts) -> Callable[[CompletionFn], Completion]:
    """Parameterized decorator for creating a simple generate function"""

    def wrapper(fn: CompletionFn):
        @turbo(**opts)
        async def generate(**kwargs):
            yield User(template=fn.__doc__, variables=kwargs)
            yield Generate()

        # @wraps(fn)
        async def wrapped(**kwargs) -> str:
            # Ensure args
            assert ensure_args(fn, kwargs)

            # Get result
            result = await generate(**kwargs).run()

            return result.content

        return wrapped

    return wrapper

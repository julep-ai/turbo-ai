from functools import wraps
import inspect
from typing import (
    Awaitable,
    Callable,
    Protocol,
    TypeVar,
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

T = TypeVar("T")


class CompletionFn(Protocol):
    def __call__(self, *args, **kwargs) -> Awaitable[None]:
        ...


class Completion(Protocol[T]):
    def __call__(self, *args, **kwargs) -> Awaitable[T]:
        ...


ParseFn = Callable[[str], T]


# Decorator
def completion(
    parse: ParseFn[T] = lambda s: str(s),
    **opts,
) -> Callable[[CompletionFn], Completion[T]]:
    """Parameterized decorator for creating a simple generate function"""

    def wrapper(fn: CompletionFn):
        @turbo(original_fn=fn, **opts)
        async def generate(**kwargs):
            yield User(template=inspect.getdoc(fn), variables=kwargs)
            yield Generate()

        @wraps(fn)
        async def wrapped(*args, **kwargs) -> str:
            params = inspect.signature(fn).bind(*args, **kwargs)
            opts = params.arguments

            # Ensure args
            assert ensure_args(fn, opts)

            # Get result
            result = await generate(**opts).run()

            return parse(result.content)

        return wrapped

    return wrapper

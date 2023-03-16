from typing import (
    Optional,
    Tuple,
    Union,
)


from .types import (
    Assistant,
    GetUserInput,
    TurboGen,
)

from .errors import GeneratorAlreadyExhausted, GeneratorAlreadyExhaustedError

__all__ = [
    "run",
]


async def run(
    gen: TurboGen,
    input: Optional[str] = None,
) -> Tuple[Union[Assistant, GetUserInput], bool]:
    """Run a turbo app"""

    # Set placeholder values
    done = False
    output = GeneratorAlreadyExhausted()

    # Run generator
    try:
        while not isinstance(output := await gen.asend(input), GetUserInput):
            pass

    # Generator exhausted, mark done
    except StopAsyncIteration:
        done = True

    # Output is still placeholder? Raise error
    if isinstance(output, GeneratorAlreadyExhausted):
        raise GeneratorAlreadyExhaustedError()

    return (output, done)

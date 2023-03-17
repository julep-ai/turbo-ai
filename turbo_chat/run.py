from typing import Optional, Tuple, Union

from .structs import GetInput, Assistant

from .errors import GeneratorAlreadyExhausted, GeneratorAlreadyExhaustedError
from .types import TurboGen

__all__ = [
    "run",
]


async def run(
    gen: TurboGen,
    input: Optional[str] = None,
) -> Tuple[Union[Assistant, GetInput], bool]:
    """Run a turbo app"""

    # Set placeholder values
    done = False
    output = GeneratorAlreadyExhausted()

    # Run generator
    try:
        while not isinstance(output := await gen.asend(input), GetInput):
            pass

    # Generator exhausted, mark done
    except StopAsyncIteration:
        done = True

    # Output is still placeholder? Raise error
    if isinstance(output, GeneratorAlreadyExhausted):
        raise GeneratorAlreadyExhaustedError()

    return (output, done)

from typing import cast, Optional

from .structs import Result

from .errors import GeneratorAlreadyExhausted, GeneratorAlreadyExhaustedError
from .types import TurboGen

__all__ = [
    "run",
]


async def run(
    gen: TurboGen,
    input: Optional[str] = None,
) -> Result:
    """Run a turbo app"""

    # Set placeholder values
    done = False
    output = GeneratorAlreadyExhausted()

    # Run generator
    try:
        while not (output := await gen.asend(input)).needs_input:
            pass

    # Generator exhausted, mark done
    except StopAsyncIteration:
        done = True

    # Output is still placeholder? Raise error
    if isinstance(output, GeneratorAlreadyExhausted):
        raise GeneratorAlreadyExhaustedError()

    # Set result values
    result = cast(Result, output)
    result.done = done

    return result

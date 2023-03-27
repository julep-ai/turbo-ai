from typing import cast, Union

from .structs import Result, Start

from .errors import GeneratorAlreadyExhausted, GeneratorAlreadyExhaustedError
from .types import TurboGenWrapper

__all__ = [
    "run",
]


async def run(
    gen: TurboGenWrapper,
    input: Union[str, dict],
) -> Result:
    """Run a turbo app"""

    # Set placeholder values
    done = False
    output = GeneratorAlreadyExhausted()

    # Run generator
    try:
        while (output := await gen.asend(input)):
            if isinstance(output, Start):
                continue

            if output.needs_input:
                break

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

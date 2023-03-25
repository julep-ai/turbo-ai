from typing import cast, Optional, Union

from .structs import Result

from .errors import GeneratorAlreadyExhausted, GeneratorAlreadyExhaustedError
from .types import TurboGenWrapper

__all__ = [
    "run",
]


async def run(
    gen: TurboGenWrapper,
    input: Optional[Union[str, dict]] = None,
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

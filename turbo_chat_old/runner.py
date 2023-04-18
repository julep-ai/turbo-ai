from typing import cast, Union

from .structs import Result, Start

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
    output = Result(content=None)
    run_count = 0

    # Run generator
    try:
        while output := await gen.asend(input):
            run_count += 1

            if isinstance(output, Start):
                continue

            if output.needs_input or output.original_role == "result":
                break

    # Generator exhausted, mark done
    except StopAsyncIteration:
        done = True

    # Set result values
    result = cast(Result, output)
    result.done = done

    return result

import pydantic

__all__ = [
    "InvalidValueYieldedError",
    "GeneratorAlreadyExhaustedError",
]


# Models
class InvalidValueYieldedError(ValueError):
    """Invalid value yielded by generator"""

    ...


class GeneratorAlreadyExhaustedError(StopAsyncIteration):
    """Generator was already exhausted"""

    ...


# Placeholder classes
class GeneratorAlreadyExhausted(pydantic.BaseModel):
    """Placeholder value to indicate that the generator was already exhausted"""

    ...

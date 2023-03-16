import pydantic


__all__ = [
    "Generate",
    "GetUserInput",
]


# Signal classes
class Generate(pydantic.BaseModel, extra=pydantic.Extra.allow):
    """Placeholder value to indicate that completion should be run"""

    yield_downstream: bool = True


class GetUserInput(pydantic.BaseModel):
    """Placeholder value to indicate that user input is needed"""

    message: str = "User input needed"

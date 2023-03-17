import pydantic


__all__ = [
    "Generate",
    "GetInput",
]


# Signal classes
class Generate(pydantic.BaseModel, extra=pydantic.Extra.allow):
    """Placeholder value to indicate that completion should be run"""

    forward: bool = True


class GetInput(pydantic.BaseModel):
    """Placeholder value to indicate that user input is needed"""

    content: str = "User input needed"

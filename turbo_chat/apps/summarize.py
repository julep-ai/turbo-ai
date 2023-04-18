from ..completion import completion

__all__ = [
    "summarize",
]


@completion(temperature=0.5)
async def summarize(text: str, text_type: str = "text"):
    """
    Summarize the following {{text_type}}:

    {{text}}
    """
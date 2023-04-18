from ..completion import completion

__all__ = [
    "qa",
]

@completion(temperature=0.1)
async def qa(question: str, context: str):
    """
    Answer the question based on the context below.

    START CONTEXT
    {{context}}
    END CONTEXT

    {{question}}
    """

from ..structs import Generate, User
from ..turbo import turbo

__all__ = [
    "qa_bot",
]

# Templates
TEMPLATE = """
Answer the question based on the context below.

START CONTEXT
{{context}}
END CONTEXT

{{question}}
""".strip()


@turbo(temperature=0.1)
async def qa_bot(question: str, context: str):
    """Takes a question and context as input and generate answer based on them"""

    yield User(
        template=TEMPLATE,
        variables=dict(question=question, context=context),
    )

    yield Generate()

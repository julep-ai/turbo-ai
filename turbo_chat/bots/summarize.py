from ..structs import Generate, User
from ..turbo import turbo

__all__ = [
    "summarize_bot",
]

# Templates
SUMMARIZE_TEMPLATE = """
Summarize the following {{text_type}}:

{{text}}
""".strip()


@turbo(model="gpt-3.5-turbo", temperature=0.2)
async def summarize_bot(text: str, text_type: str = "text"):
    yield User(
        template=SUMMARIZE_TEMPLATE,
        variables=dict(text=text, text_type=text_type),
    )

    yield Generate()

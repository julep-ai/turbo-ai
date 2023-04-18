from typing import List, Tuple

from ..structs import Result
from ..turbo import turbo
from ..types.generators import TurboGenFn
from .subqueries import subqueries_bot

__all__ = [
    "self_ask_bot",
]


# Utils
def make_qa_context(qa_context, previous_qa):
    """Prepare qa context."""

    # Add previous q&a as faq
    if len(previous_qa):
        qas = "\n\n".join([f"Q: {q}\nA: {a}" for q, a in previous_qa])

        qa_context += "FAQ:\n"
        qa_context += qas

    return qa_context


@turbo(temperature=0.7)
async def self_ask_bot(
    question: str,
    context: str,
    qa_bot: TurboGenFn,
    subquery_instructions: str = "User is asking questions to an AI assistant.",
):
    """Takes a question and qa_bot and uses them to answer step by step."""

    # Generate sub queries
    queries = await subqueries_bot(
        request=question,
        context=subquery_instructions,
    ).run()

    # Answer sub-questions
    previous_qa: List[Tuple[str, str]] = []

    for query in [*queries.content, question]:
        # Generate new answer
        answer = await qa_bot(
            question=query,
            context=make_qa_context(context, previous_qa),
        ).run()

        # Append query and answer to list
        previous_qa.append((query, answer.content))

    # Yield the last answer as the result
    yield Result(content=previous_qa[-1][-1])

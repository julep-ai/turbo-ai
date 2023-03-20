from typing import List

from ...structs import Generate, Result, User
from ...turbo import turbo
from .scratchpad import scratchpad
from .template import SUBQUERIES_TEMPLATE

__all__ = [
    "subqueries_bot",
]

default_subqueries_example: str = """
Context:
User is a customer at a grocery store and is asking the question to the store manager.

Question:
What is the least expensive cereal that is healthy and has a low calorie content but is also tasty?

Thoughts:
- The user wants to know about "tasty but healthy cereal".
- The question requires looking up cereal by nutrition value and price
- In order to "What is the least expensive cereal that is healthy and has a low calorie content but is also tasty?" for the user, we need to first ask the knowledgebase the following queries:

Queries to execute:
1. What are some tasty cereal that are healthy?
2. What are the prices of the above cereals?
3. What is the least expensive cereal of the above?
""".strip()  # noqa: E501


@turbo(model="gpt-4")
async def subqueries_bot(
    request: str,
    context: str,
    example: str = default_subqueries_example,
    max_queries: int = 6,
    request_type: str = "question",
    solve_act: str = "answer",
):
    """Bot that decomposes a request into sub queries for a knowledgebase."""

    # Yield instructions
    yield User(
        template=SUBQUERIES_TEMPLATE,
        variables=dict(
            request=request,
            context=context,
            example=example,
            max_queries=max_queries,
            request_type=request_type,
            solve_act=solve_act,
        ),
    )

    # Generate output
    output = yield Generate(forward=False)

    # Parse output
    parsed_queries = scratchpad.parse(output.content)
    queries: List[str] = [
        query for query in parsed_queries.values() if query is not None
    ]

    yield Result(content=queries)

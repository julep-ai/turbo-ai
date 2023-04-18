from ...completion import completion
from .scratchpad import scratchpad


__all__ = [
    "subqueries",
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


@completion(temperature=0, parse=scratchpad.parse)
async def subqueries(
    request: str,
    context: str,
    example: str = default_subqueries_example,
    max_queries: int = 6,
    request_type: str = "question",
    solve_act: str = "answer",
):
    """
    {% set _request_type = request_type or "question" -%}
    {% set _solve_act = solve_act or "answer" -%}
    {% set _max_queries = max_queries or 6 -%}
    Your task is to create a plan to collect information for {{_solve_act | inflect("VBG")}} a complex {{_request_type}}.
    You have at your disposal a knowledgebase that can give answers to plain english queries.
    Based on the given {{_request_type}} and the context below, write a list of simple, standalone queries to ask the knowledgebase in order to collect all the information necessary to {{_solve_act}} that {{_request_type}}.
    You do not have to {{_solve_act}} the {{_request_type}}, just come up with a step by step plan to collect information to do so.

    Instructions:
    1. First think step by step to break down the {{_request_type}} into individual queries.
    2. Use the format below to think through and write your thoughts.
    3. Write down the knwoledgebase queries as a numbered list under the heading: "Queries to execute:"
    4. Each query MUST be concise and standalone.
    5. Do not come up with more than {{_max_queries}} queries.
    6. The queries will be executed verbatim so make sure to resolve all coreferences and add contextual information.

    Format for writing down your thoughts and the queries:

    ```
    Thoughts:
    - The {{_request_type}} is about "<topic>"
    - The {{_request_type}} requires looking up ...
    - ... other thoughts
    - In order to {{_solve_act}} "<{{_request_type}}>" for the user, we need to first ask the knowledgebase the following queries.

    Queries to execute:
    1. <query 1>
    2. <query 3>
    and so on...

    For example,

    START EXAMPLE
    {{example}}
    END EXAMPLE

    ---

    Begin!

    Context:
    {{context}}

    {{_request_type | capitalize}}:
    {{request}}
    ```
    """  # noqa: E501
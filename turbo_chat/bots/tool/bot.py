from typing import List, Optional

from ...structs import Assistant, GetInput, Generate, Result, User
from ...turbo import turbo
from ...types import Tool
from .scratchpad import scratchpad
from .template import EXAMPLE_TEMPLATE, TOOLBOT_TEMPLATE

default_tool_example: str = """
Customer said: Where is the store located?
Thought: Use another tool to get information? Yes
Tool: GetInformation
Tool Input: {"question": "What is the address of the store?"}
Tool Result: The address of [STORE NAME] is [SOME ADDRESS]
Thought: Use another tool to get information? No
Response: [STORE NAME] is located at [SOME ADDRESS].
""".strip()


@turbo(model="gpt-3.5-turbo", temperature=0.7)
async def tool_bot(
    tools: List[Tool],
    prologue: Optional[str] = None,
    user_type: str = "user",
    instruction: Optional[str] = None,
    additional_info: Optional[str] = None,
    example: str = default_tool_example,
    max_iterations: int = 6,

    # Placeholder for message to send to the user
    message: str = "How can I help you?",
):
    # Yield instructions
    yield User(
        template=TOOLBOT_TEMPLATE,
        variables=dict(
            tools=tools,
            prologue=prologue,
            user_type=user_type,
            instruction=instruction,
            additional_info=additional_info,
        ),
        # check=True,  # FIXME: Throws an error, possible bug in jinja2schema
    )

    # Yield example
    yield User(template=EXAMPLE_TEMPLATE, variables={"example": example})

    # Get user input
    input = yield GetInput(content=message)
    yield User(content=f"{user_type} said: {input}")

    # Start the tool agent
    parsed_tools = {}
    iterations_left = max_iterations
    tools_used = []

    # Keep running until we get final response
    while "final_response" not in parsed_tools and iterations_left > 0:
        iterations_left -= 1

        output = yield Generate(stop=["Tool Result"], forward=False)
        parsed_tools = scratchpad.parse(output.content)

        # If no tool required to run, continue
        if not parsed_tools.get("tool_name"):
            continue

        # Otherwise run tool
        # First check if tool is valid
        selected_tool = parsed_tools["tool_name"]
        tool_names = [tool.__name__ for tool in tools]

        if selected_tool not in tool_names:
            yield User(
                content=(
                    f"Tool Result: `{selected_tool}` is not a valid tool."
                    f"Pick one from [{', '.join(tool_names)}]."
                )
            )

            continue

        # Tool is valid. Run it
        tools_used.append(selected_tool)

        # Get tool input
        tool_fn = next(tool for tool in tools if tool.__name__ == selected_tool)
        tool_input = parsed_tools.get("tool_input") or {}

        # Run tool
        tool_result = await tool_fn(**tool_input)

        # Yield the observation
        yield Assistant(content=f"Tool Result: {tool_result.strip()}")

    # Yield final response if any
    response = parsed_tools.get(
        "final_response",
        "I am not sure how to answer this question",
    )

    yield Result(content=dict(response=response, tools_used=tools_used))

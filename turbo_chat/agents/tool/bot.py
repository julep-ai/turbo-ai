from typing import List, Literal, Optional

from ...structs import Example, GetInput, Generate, Result, User
from ...turbo import turbo
from ...types import Tool, ToolBotInput
from .scratchpad import scratchpad
from .template import TOOLBOT_TEMPLATE

default_tool_example: str = """
Customer said: Where is the store located?
Thought: Use another tool to get information? Yes
Tool: GetInformation
Tool Input: {"question": "What is the address of the store?"}
Tool Result: The address of [STORE NAME] is [SOME ADDRESS]
Thought: Use another tool to get information? No
Response: [STORE NAME] is located at [SOME ADDRESS].
""".strip()


@turbo(temperature=0)
async def tool_bot(
    tools: List[Tool],
    prologue: Optional[str] = None,
    user_type: str = "user",
    instruction: Optional[str] = None,
    initial_state: Optional[str] = None,
    example: str = default_tool_example,
    max_iterations: int = 6,
    state_message_position: Literal["top", "bottom"] = "top",
    # Placeholder for message to send to the user
    message: str = "How can I help you?",
):
    # Capitalize user_type
    user_type = user_type.strip().capitalize()

    # Yield initial state
    if initial_state:
        yield User(
            content=initial_state,
            sticky=True,
            sticky_position=state_message_position,
            label="state",
        )

    # Yield instructions
    yield User(
        template=TOOLBOT_TEMPLATE,
        variables=dict(
            tools=tools,
            prologue=prologue,
            user_type=user_type,
            instruction=instruction,
        ),
        # check=True,  # FIXME: Throws an error, possible bug in jinja2schema
    )

    # Yield example
    # yield User(template=EXAMPLE_TEMPLATE, variables={"example": example})
    example_user_line, *example_assistant_lines = example.splitlines()
    yield Example(
        user=example_user_line,
        assistant="\n".join(example_assistant_lines),
    )

    while True:
        # Get user input
        data: ToolBotInput = yield GetInput(content=message)
        input: str = data["input"]
        state: Optional[str] = data.get("state")

        # Yield user input and state
        if state:
            yield User(
                content=state,
                sticky=True,
                sticky_position=state_message_position,
                label="state",
            )

        yield User(content=f"{user_type} said: {input}")

        # Start the tool agent
        parsed_tools = {}
        iterations_left = max_iterations
        tools_used = []

        # Keep running until we get final response
        while "final_response" not in parsed_tools and iterations_left > 0:
            iterations_left -= 1

            output = yield Generate(
                stop=["Tool Result", f"{user_type} said:"],
                forward=False,
            )

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
            yield User(content=f"Tool Result: {tool_result.strip()}")

        # Yield final response if any
        response = parsed_tools.get(
            "final_response",
            "I am not sure how to answer this question",
        )

        yield Result(content=dict(response=response, tools_used=tools_used))

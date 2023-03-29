# flake8: noqa
from ward import test

from turbo_chat import *
from turbo_chat.bots import tool_bot
from turbo_chat.utils.pprint import pprint_color

first_name = "Lady"
last_name = "Gaga"


async def GetMyFirstName():
    """Use this tool to get my first name"""
    return first_name


app = tool_bot.configure(debug=pprint_color)(
    tools=[GetMyFirstName], initial_state="My last name is Antebellum"
)


@test("contains returns True when toolbot works")
async def test_toolbot():
    await app.run()
    result = await app.run(
        {
            "input": "What is my first and last name?",
            "state": f"My last name is {last_name}",
        }
    )

    assert isinstance(result.content, dict)
    assert "GetMyFirstName" in result.content["tools_used"]
    assert first_name.lower() in result.content["response"].lower()
    assert last_name.lower() in result.content["response"].lower()

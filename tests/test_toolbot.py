# flake8: noqa
from ward import test

from turbo_chat import *
from turbo_chat.bots import tool_bot


@test("contains returns True when toolbot works")
async def test_toolbot():
    name = "Gaga"

    async def GetMyName(_):
        """Use this tool to get my name"""
        return name

    app = tool_bot(tools=[GetMyName])
    await app.run()
    result = await app.run("What is my name?")

    assert "gaga" in result.content.lower()

# flake8: noqa
from ward import test

from turbo_chat import *


@test("contains returns True when toolbot works")
async def test_toolbot():
    name = "Lady Gaga"

    async def GetMyName(_):
        """Use this tool to get my name"""
        return name

    app = tool_bot(tools=[GetMyName])
    await run(app)
    result = await run(app, "What is my name?")

    assert "lady gaga" in result.content.lower()

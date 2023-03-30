# flake8: noqa
from ward import test

from turbo_chat import *


@test("contains returns True when memory injection works")
async def test_memory_injection():
    @turbo()
    async def example(zodiac: str, memory):
        yield System(content="You are a fortune teller")

        messages = await memory.get()
        assert len(messages)

    b = await example(zodiac="pisces").init()
    await b.run()

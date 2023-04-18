# flake8: noqa
from ward import test

from turbo_chat import *


@test("contains returns True when memory injection works")
async def test_memory_injection():
    @turbo()
    async def example(memory):
        yield System(content="You are a fortune teller")

        messages = await memory.get()
        assert len(messages)

    await example().run()

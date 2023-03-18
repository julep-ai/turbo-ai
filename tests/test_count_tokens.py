# flake8: noqa
from ward import test

from turbo_chat import *


@test("contains returns True when count tokens works")
async def test_turbo():
    @turbo()
    async def example(zodiac: str, memory):
        yield System(content="You are a fortune teller")
        yield Generate()

        messages = await memory.get()
        num_tokens = await memory.count_tokens()
        assert num_tokens

    b = example(zodiac="pisces")
    await run(b)

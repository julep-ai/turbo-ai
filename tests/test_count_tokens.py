# flake8: noqa
from ward import test

from turbo_chat import *
from turbo_chat.utils.tokens import count_tokens


@test("contains returns True when count tokens works")
async def test_turbo():
    @turbo()
    async def example(zodiac: str, memory):
        yield System(content="You are a fortune teller")
        yield Generate()

        messages = await memory.get_dicts()
        num_tokens = count_tokens(messages, memory.model)
        assert num_tokens

    b = example(zodiac="pisces")
    await b.run()

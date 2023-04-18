# flake8: noqa
from ward import test

from turbo_chat import *
from turbo_chat.utils.tokens import count_tokens, get_max_tokens_length


@test("contains returns True when memory filter works")
async def test_memory_filter():
    @turbo(memory_class=LocalTruncatedMemory)
    async def example(memory):
        for _ in range(50_000):
            yield System(content="You are a fortune teller")

        messages = await memory.prepare_prompt()
        num_tokens = count_tokens(messages, memory.model)
        assert num_tokens < get_max_tokens_length(memory.model)

    await example().run()

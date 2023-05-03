# flake8: noqa
from ward import test

from turbo_chat import *
from turbo_chat.utils.tokens import count_tokens, get_max_tokens_length


@test("contains returns True when memory filter works")
async def test_memory_filter():
    @turbo(memory_class=LocalTruncatedMemory)
    async def example(zodiac: str, memory):
        for _ in range(50_000):
            yield User(content="You are a fortune teller" * 500)

        messages = await memory.prepare_prompt()
        num_tokens = count_tokens(messages, memory.model)
        assert num_tokens < get_max_tokens_length(memory.model)

    await example(zodiac="pisces").run()

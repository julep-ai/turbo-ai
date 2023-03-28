# flake8: noqa
from ward import test

from turbo_chat import *
from turbo_chat.utils.tokens import count_tokens, get_max_tokens_length


@test("contains returns True when memory filter works")
async def test_memory_filter():
    @turbo(memory_class=LocalTruncatedMemory)
    async def example(zodiac: str, memory):
        yield ExampleAssistant(content="Hello")
        yield Assistant(content="You are a fortune teller")

        messages = await memory.prepare_prompt()
        assert messages[0]["role"] == "system name=example_assistant"

    await example(zodiac="pisces").run()

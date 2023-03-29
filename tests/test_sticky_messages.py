# flake8: noqa
from ward import test

from turbo_chat import *


@test("contains returns True when sticky messages work")
async def test_turbo():
    @turbo()
    async def example(zodiac: str, memory):
        for i in range(20):
            yield User(
                content=f"Hello {i}",
                sticky=True,
                label="user",
                sticky_position="bottom",
            )
            yield System(
                content="You are a fortune teller",
                sticky=True,
                label="system",
                sticky_position="top",
            )
            yield Assistant(content="Hi")

        messages = await memory.prepare_prompt()
        assert len(messages) == 20 + 1 + 1
        assert messages[0]["content"] == "You are a fortune teller"
        assert messages[-1]["content"] == "Hi"
        assert messages[-2]["content"] == "Hello 19"

    b = await example(zodiac="pisces").init()
    await b.run()

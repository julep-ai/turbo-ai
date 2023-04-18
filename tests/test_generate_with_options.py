# flake8: noqa
from ward import test

from turbo_chat import *


@test("contains returns True when Generate options work")
async def test_generate_options():
    @turbo()
    async def example():
        yield System(content="You are a good guy named John")
        yield User(
            content="What is your name?",
            generate_kwargs={"stop": "John"},
            yield_as_result=True,
        )

    output = await example().run()

    assert "john" not in output.content_str.lower()

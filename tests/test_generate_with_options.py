# flake8: noqa
from ward import test

from turbo_chat import *


@test("contains returns True when Generate options work")
async def test_generate_options():
    @turbo()
    async def example():
        yield System(content="You are a good guy named John")
        yield User(content="What is your name?")
        result = yield Generate(stop="John")

    b = await example().init()
    results = [output.content async for output in b]
    results_str = "".join(results)

    assert "john" not in results_str.lower()

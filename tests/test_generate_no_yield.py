# flake8: noqa
from ward import test

from turbo_chat import *


@test("contains returns True when User yield_as_result=True works")
async def test_generate_yield_as_result():
    lady = "gaga"

    @turbo()
    async def example():
        yield System(content="You are a good guy named John")
        yield User(
            content="What is your name?",
            yield_as_result=True,
        )
        
        nonlocal lady
        lady = "finger"

    await example().run()

    assert lady == "gaga"

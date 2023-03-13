# flake8: noqa
from ward import test

from turbo_chat import *


@test("contains returns True when original fn correctly set")
async def test_turbo():
    async def example(context):
        yield System(content="You are a fortune teller")
        yield User(content=f"My zodiac sign is {context['zodiac']}")

        input = yield GetUserInput(message="What do you want to know?")
        yield User(content=input)

        value = yield Generate(settings={"temperature": 0.9})
        print(f"generated: {value}")

    original_fn = example

    # Emulate decorator
    example = turbo()(example)
    assert example.fn == original_fn

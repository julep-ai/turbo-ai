# flake8: noqa
from ward import test

from turbo_chat import *


@test("contains returns True when turbo works")
async def test_turbo():
    @turbo()
    async def example(zodiac: str):
        yield System(content="You are a fortune teller")
        yield User(content=f"My zodiac sign is {zodiac}")

        input = yield GetInput(content="What do you want to know?")
        yield User(content=input)

        value = yield Generate(temperature=0.9)

    b = example(zodiac="pisces")
    output = await b.run()

    assert isinstance(output, Result)
    assert not output.done

    output = await b.run("Tell me my fortune")
    assert isinstance(output, Result)
    assert output.done


@test("contains returns True when turbo with positional args works")
async def test_turbo_positional_args():
    @turbo()
    async def example(zodiac: str):
        yield System(content="You are a fortune teller")
        yield User(content=f"My zodiac sign is {zodiac}")

        input = yield GetInput(content="What do you want to know?")
        yield User(content=input)

        value = yield Generate(temperature=0.9)

    b = example("pisces")
    output = await b.run()

    assert isinstance(output, Result)
    assert not output.done

    output = await b.run("Tell me my fortune")
    assert isinstance(output, Result)
    assert output.done

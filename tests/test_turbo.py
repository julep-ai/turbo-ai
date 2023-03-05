# flake8: noqa
from ward import test

from turbo_chat import *


@test("contains returns True when turbo works")
async def test_turbo():
    @turbo()
    async def example(context):
        yield System(content="You are a fortune teller")
        yield User(content=f"My zodiac sign is {context['zodiac']}")

        input = yield GetUserInput(message="What do you want to know?")
        yield User(content=input)

        value = yield Generate(settings={"temperature": 0.9})
        print(f"generated: {value}")

    b = example({"zodiac": "pisces"})
    output, done = await run(b)
    print((output, done))
    assert isinstance(output, GetUserInput)
    assert not done

    output, done = await run(b, "Tell me my fortune")
    print((output, done))
    assert isinstance(output, Assistant)
    assert done

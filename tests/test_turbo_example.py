# flake8: noqa
from ward import test

from typing import AsyncGenerator, Union

from turbo_chat import (
    turbo,
    System,
    User,
    Assistant,
    GetUserInput,
    Generate,
    run,
)


def input(*args):
    return "Tell me my horoscope"


@test("contains returns True when the example works")
async def test_turbo_example():
    # Get user
    async def get_user(id):
        return {"zodiac": "pisces"}

    # Set user zodiac mixin
    # Notice that no `@turbo()` decorator used here
    async def set_user_zodiac(user_id: int):
        user_data: dict = await get_user(user_id)
        zodiac: str = user_data["zodiac"]

        yield User(content=f"My zodiac sign is {zodiac}")

    # Horoscope app
    @turbo(temperature=0.0)
    async def horoscope(user_id: int):
        yield System(content="You are a fortune teller")

        # Yield from mixin
        async for output in set_user_zodiac(user_id):
            yield output

        # Prompt runner to ask for user input
        input = yield GetUserInput(message="What do you want to know?")

        # Yield the input
        yield User(content=input)

        # Generate (overriding the temperature)
        value = yield Generate(temperature=0.9)

    # Let's run this
    app: AsyncGenerator[Union[Assistant, GetUserInput], str] = horoscope(user_id=1)

    _input = None
    while response := await run(app, _input):
        result, done = response

        if isinstance(result, GetUserInput):
            _input = input(result.message)
            continue

        if isinstance(result, Assistant):
            print(result.content)

        if done:
            break

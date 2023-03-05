# turbo-chat

> Idiomatic way to build chatgpt apps using async generators in python

The [ChatGPT API](https://openai.com/blog/introducing-chatgpt-and-whisper-apis) uses a new input format called [chatml](https://github.com/openai/openai-python/blob/main/chatml.md). In openai's [python client](https://github.com/openai/openai-python/blob/main/chatml.md), the format is used something like this:

```python
messages = [
    {"role": "system", "content": "Greet the user!"},
    {"role": "user", "content": "Hello world!"},
]
```

The idea here is to incrementally build the messages using an async generator and then use that to generate completions. [Async generators](https://superfastpython.com/asynchronous-generators-in-python/) are incredibly versatile and simple abstraction for doing this kind of stuff. They can also be composed together very easily.

```python
# Equivalent turbo-chat generator
async def example():
    yield System(content="Greet the user!")
    yield User(content="Hello World!")

    # To run generation, just yield Generate(),
    # the lib will take care of correctly running the app, and
    # return the value back here.
    output = yield Generate()
    print(output.content)
```

See more detailed example below.

## Installation

```bash
pip install turbo-chat
```

## Example

```python
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

# Get user
async def get_user(id):
    return {"zodiac": "pisces"}

# Set user zodiac mixin
@turbo()
async def set_user_zodiac(context: dict):

    user_id: int = context["user_id"]
    user_data: dict = await get_user(user_id)
    zodiac: str = user_data["zodiac"]

    yield User(content=f"My zodiac sign is {zodiac}")


# Horoscope app
@turbo()
async def horoscope(context: dict):

    yield System(content="You are a fortune teller")

    while response := await run(set_user_zodiac(context)):
        output, done = response
        yield output
        if done:
            break

    # Prompt runner to ask for user input
    input = yield GetUserInput(message="What do you want to know?")

    # Yield the input
    yield User(content=input)

    # Generate (overriding the temperature)
    value = yield Generate(settings={"temperature": 0.9})


# Let's run this
app: AsyncGenerator[Union[Assistant, GetUserInput], str] = horoscope({"user_id": 1})

_input = None
while True:
    result, done = await run(app, _input)

    if isinstance(result, GetUserInput):
        _input = input(result.message)
        continue

    if isinstance(result, Assistant):
        print(result.content)

    if done:
        break
```

You can also customize how the messages are persisted in-between the executions.

```python
from turbo_chat import turbo, BaseMemory

class RedisMemory(BaseMemory):
    """Implement BaseMemory methods here"""

    async def init(self, context) -> None:
        ...

    async def append(self, item) -> None:
        ...

    async def clear(self) -> None:
        ...


# Now use the memory in a turbo_chat app
@turbo(memory=RedisMemory())
async def app():
    ...
```

---

![turbo](https://user-images.githubusercontent.com/931887/222912628-8662fad0-091f-4cb8-92f3-6cce287716e9.jpg)

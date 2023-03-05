# turbo-chat

> Idiomatic way to build chatgpt apps using async generators in python

The [ChatGPT API](https://openai.com/blog/introducing-chatgpt-and-whisper-apis) uses a new input format called [chatml](https://github.com/openai/openai-python/blob/main/chatml.md). In openai's [python client](https://github.com/openai/openai-python/blob/main/chatml.md), the format is used something like this:

```python
messages = [
    {"role": "system", "content": "Greet the user!"},
    {"role": "user", "content": "Hello world!"},
]
```

The idea here is to incrementally build the messages using an async generator and then use that to generate completions. [Async generators](https://superfastpython.com/asynchronous-generators-in-python/) are incredibly versatile and simple abstraction for doing this kind of stuff. They can also be composed together very easily. See example below.

## Installation

```bash
pip install turbo-chat
```

## Example

```python
from typing import AsyncGenerator

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

    yield User(content=f"My zodiac sign is {context['zodiac']}")


# Horoscope app
@turbo()
async def horoscope(context: dict):

    yield System(content="You are a fortune teller")

    async for (output, _) in run(set_user_zodiac()):
        yield output

    # Prompt runner to ask for user input
    input = yield GetUserInput(message="What do you want to know?")

    # Yield the input
    yield User(content=input)

    # Generate (overriding the temperature)
    value = yield Generate(settings={"temperature": 0.9})


# Let's run this
app: AsyncGenerator[Assistant | GetUserInput, str] = horoscope({"user_id": 1})

_input = None
while True:
    result, done = await run(app, _input)

    if isinstance(result, GetUserInput):
        _input = raw_input(result.message)
        continue

    if isinstance(result, Assistant):
        print(result.content)

    if done:
        break
```

---

![turbo](https://user-images.githubusercontent.com/931887/222912628-8662fad0-091f-4cb8-92f3-6cce287716e9.jpg)

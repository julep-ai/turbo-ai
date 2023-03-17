# turbo-chat

> Idiomatic way to build chatgpt apps using async generators in python

![turbo](https://user-images.githubusercontent.com/931887/222912628-8662fad0-091f-4cb8-92f3-6cce287716e9.jpg)

## About

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
    GetInput,
    Generate,
    run,
)

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
    input = yield GetInput(message="What do you want to know?")

    # Yield the input
    yield User(content=input)

    # Generate (overriding the temperature)
    value = yield Generate(temperature=0.9)

# Let's run this
app: AsyncGenerator[Union[Assistant, GetInput], str] = horoscope({"user_id": 1})

_input = None
while not (result := await run(app, _input)).done:
    if result.needs_input:
        # Prompt user with the input message
        _input = input(result.content)
        continue

    print(result.content)

# Output
# >>> What do you want to know? Tell me my fortune
# >>> As an AI language model, I cannot predict the future or provide supernatural fortune-telling. However, I can offer guidance and advice based on your current situation and past experiences. Is there anything specific you would like me to help you with?
#

```

### Custom memory

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
@turbo(memory_class=RedisMemory)
async def app():
    ...
```

### Get access to memory object directly (just declare an additional param)

```python
@turbo()
async def app(some_param: Any, memory: BaseMemory):

    messages = await memory.get()
    ...
```

### Generate a response to use internally but don't yield downstream

```python
@turbo()
async def example():
    yield System(content="You are a good guy named John")
    yield User(content="What is your name?")
    result = yield Generate(forward=False)

    yield User(content="How are you doing?")
    result = yield Generate()

b = example()
results = [output async for output in b]

assert len(results) == 1
```

### Add a simple in-memory cache

You can also subclass the `BaseCache` class to create a custom cache.

```python
cache = SimpleCache()

@turbo(cache=cache)
async def example():
    yield System(content="You are a good guy named John")
    yield User(content="What is your name?")
    result = yield Generate()

b = example()
results = [output async for output in b]

assert len(cache.cache) == 1

```

---

### Latest Changes

* Update README.md. PR [#11](https://github.com/creatorrr/turbo-chat/pull/11) by [@creatorrr](https://github.com/creatorrr).


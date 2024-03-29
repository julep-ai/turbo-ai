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
while not (result := await (app.run(_input)).done:
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

    async def setup(self, **kwargs) -> None:
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

* fix: Fix cache not saving to memory. PR [#63](https://github.com/creatorrr/turbo-chat/pull/63) by [@creatorrr](https://github.com/creatorrr).
* version: 0.3.11. PR [#62](https://github.com/creatorrr/turbo-chat/pull/62) by [@creatorrr](https://github.com/creatorrr).
* fix: Fix truncation. PR [#61](https://github.com/creatorrr/turbo-chat/pull/61) by [@creatorrr](https://github.com/creatorrr).
* version: 0.3.10. PR [#60](https://github.com/creatorrr/turbo-chat/pull/60) by [@creatorrr](https://github.com/creatorrr).
* version: 0.3.9. PR [#59](https://github.com/creatorrr/turbo-chat/pull/59) by [@creatorrr](https://github.com/creatorrr).
* x/fix cache args. PR [#58](https://github.com/creatorrr/turbo-chat/pull/58) by [@creatorrr](https://github.com/creatorrr).
* version: 0.3.7. PR [#57](https://github.com/creatorrr/turbo-chat/pull/57) by [@creatorrr](https://github.com/creatorrr).
* f/support multi choice. PR [#56](https://github.com/creatorrr/turbo-chat/pull/56) by [@creatorrr](https://github.com/creatorrr).
* feat: Support multiple choices selector; n > 1. PR [#55](https://github.com/creatorrr/turbo-chat/pull/55) by [@creatorrr](https://github.com/creatorrr).
* feat: Support positional arguments for running apps. PR [#54](https://github.com/creatorrr/turbo-chat/pull/54) by [@creatorrr](https://github.com/creatorrr).
* feat: Make get_encoding faster. PR [#53](https://github.com/creatorrr/turbo-chat/pull/53) by [@creatorrr](https://github.com/creatorrr).
* feat: Add ttl support to redis_cache. PR [#52](https://github.com/creatorrr/turbo-chat/pull/52) by [@creatorrr](https://github.com/creatorrr).
* feat: Support for parsing completions. PR [#51](https://github.com/creatorrr/turbo-chat/pull/51) by [@creatorrr](https://github.com/creatorrr).
* version: 0.3.6. PR [#50](https://github.com/creatorrr/turbo-chat/pull/50) by [@creatorrr](https://github.com/creatorrr).
* feat: Add RedisCache implementation. PR [#49](https://github.com/creatorrr/turbo-chat/pull/49) by [@creatorrr](https://github.com/creatorrr).
* fix: Fix json array. PR [#48](https://github.com/creatorrr/turbo-chat/pull/48) by [@creatorrr](https://github.com/creatorrr).
* version: 0.3.5. PR [#47](https://github.com/creatorrr/turbo-chat/pull/47) by [@creatorrr](https://github.com/creatorrr).
* fix: Fix how function signature and docstring was being parsed. PR [#46](https://github.com/creatorrr/turbo-chat/pull/46) by [@creatorrr](https://github.com/creatorrr).
* version: 0.3.4. PR [#45](https://github.com/creatorrr/turbo-chat/pull/45) by [@creatorrr](https://github.com/creatorrr).
* feat: Add @completion decorator. PR [#44](https://github.com/creatorrr/turbo-chat/pull/44) by [@creatorrr](https://github.com/creatorrr).
* version: 0.3.3. PR [#43](https://github.com/creatorrr/turbo-chat/pull/43) by [@creatorrr](https://github.com/creatorrr).
* feat: Memory expects memory_args, Assistant no longer yields automatically. PR [#42](https://github.com/creatorrr/turbo-chat/pull/42) by [@creatorrr](https://github.com/creatorrr).
* v/0.3.2. PR [#41](https://github.com/creatorrr/turbo-chat/pull/41) by [@creatorrr](https://github.com/creatorrr).
* version: 0.3.1. PR [#40](https://github.com/creatorrr/turbo-chat/pull/40) by [@creatorrr](https://github.com/creatorrr).
* fix: Fix scratchpad parsing. PR [#39](https://github.com/creatorrr/turbo-chat/pull/39) by [@creatorrr](https://github.com/creatorrr).
* version: 0.3.0. PR [#38](https://github.com/creatorrr/turbo-chat/pull/38) by [@creatorrr](https://github.com/creatorrr).
* x/more toolbot fixes. PR [#37](https://github.com/creatorrr/turbo-chat/pull/37) by [@creatorrr](https://github.com/creatorrr).
* version: 0.2.13. PR [#36](https://github.com/creatorrr/turbo-chat/pull/36) by [@creatorrr](https://github.com/creatorrr).
* v/0.2.12. PR [#35](https://github.com/creatorrr/turbo-chat/pull/35) by [@creatorrr](https://github.com/creatorrr).
* fix: toolbot additional_info parameter. PR [#34](https://github.com/creatorrr/turbo-chat/pull/34) by [@creatorrr](https://github.com/creatorrr).
* version: 0.2.11. PR [#33](https://github.com/creatorrr/turbo-chat/pull/33) by [@creatorrr](https://github.com/creatorrr).
* f/json tool bot. PR [#32](https://github.com/creatorrr/turbo-chat/pull/32) by [@creatorrr](https://github.com/creatorrr).
* version: 0.2.10. PR [#31](https://github.com/creatorrr/turbo-chat/pull/31) by [@creatorrr](https://github.com/creatorrr).
* feat: Add sticky messages. PR [#30](https://github.com/creatorrr/turbo-chat/pull/30) by [@creatorrr](https://github.com/creatorrr).
* version: 0.2.9. PR [#29](https://github.com/creatorrr/turbo-chat/pull/29) by [@creatorrr](https://github.com/creatorrr).
* feat: Add .init method to TurboGenWrapper. PR [#28](https://github.com/creatorrr/turbo-chat/pull/28) by [@creatorrr](https://github.com/creatorrr).
* doc: Generate FAQ using autodoc. PR [#27](https://github.com/creatorrr/turbo-chat/pull/27) by [@creatorrr](https://github.com/creatorrr).
* version: 0.2.8. PR [#26](https://github.com/creatorrr/turbo-chat/pull/26) by [@creatorrr](https://github.com/creatorrr).
* feat: Add .run() method to the TurboGen object. PR [#25](https://github.com/creatorrr/turbo-chat/pull/25) by [@creatorrr](https://github.com/creatorrr).
- version: 0.2.7. PR [#24](https://github.com/creatorrr/turbo-chat/pull/24) by [@creatorrr](https://github.com/creatorrr).
- feat: self-ask bot. PR [#23](https://github.com/creatorrr/turbo-chat/pull/23) by [@creatorrr](https://github.com/creatorrr).
- version: 0.2.6. PR [#22](https://github.com/creatorrr/turbo-chat/pull/22) by [@creatorrr](https://github.com/creatorrr).
- feat: Add summary memory. PR [#21](https://github.com/creatorrr/turbo-chat/pull/21) by [@creatorrr](https://github.com/creatorrr).
- version: 0.2.5. PR [#20](https://github.com/creatorrr/turbo-chat/pull/20) by [@creatorrr](https://github.com/creatorrr).
- version: 0.2.4. PR [#19](https://github.com/creatorrr/turbo-chat/pull/19) by [@creatorrr](https://github.com/creatorrr).
- refactor: Move trucation logic to a separate memory class. PR [#18](https://github.com/creatorrr/turbo-chat/pull/18) by [@creatorrr](https://github.com/creatorrr).
- version: 0.2.3. PR [#17](https://github.com/creatorrr/turbo-chat/pull/17) by [@creatorrr](https://github.com/creatorrr).
- f/memory improvements. PR [#16](https://github.com/creatorrr/turbo-chat/pull/16) by [@creatorrr](https://github.com/creatorrr).
- version: 0.2.2. PR [#15](https://github.com/creatorrr/turbo-chat/pull/15) by [@creatorrr](https://github.com/creatorrr).
- f/tool bot. PR [#14](https://github.com/creatorrr/turbo-chat/pull/14) by [@creatorrr](https://github.com/creatorrr).
- v/0.2.1. PR [#13](https://github.com/creatorrr/turbo-chat/pull/13) by [@creatorrr](https://github.com/creatorrr).
- feat: Add count_tokens. PR [#12](https://github.com/creatorrr/turbo-chat/pull/12) by [@creatorrr](https://github.com/creatorrr).
- Update README.md. PR [#11](https://github.com/creatorrr/turbo-chat/pull/11) by [@creatorrr](https://github.com/creatorrr).

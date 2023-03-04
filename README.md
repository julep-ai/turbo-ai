# turbo-chat

> Idiomatic way to build chatgpt apps using async generators in python

## Installation

```bash
pip install turbo-chat
```

## Example

```python
from turbo_chat import *

# Horoscope app
@turbo()
async def horoscope(context: dict):

    yield System(content="You are a fortune teller")
    yield User(content=f"My zodiac sign is {context['zodiac']}")

    input = yield GetUserInput(message="What do you want to know?")
    yield User(content=input)

    value = yield Generate(settings={"temperature": 0.9})
    print(f"generated: {value}")

# Testing
app = horoscope({"zodiac": "pisces"})

output, done = await run(app)
assert isinstance(output, GetUserInput)
assert not done

user_input = "Tell me my fortune"
output, done = await run(app, user_input)
assert isinstance(output, str)
assert done
```

![turbo](https://user-images.githubusercontent.com/931887/222912628-8662fad0-091f-4cb8-92f3-6cce287716e9.jpg)

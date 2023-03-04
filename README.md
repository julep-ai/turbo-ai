# turbo-chat

> Idiomatic way to build chatgpt apps using async generators in python

## Example

```python
from turbo_chat import *

@turbo()
async def horoscope(context):

    yield System(content="You are a fortune teller")
    yield User(content=f"My zodiac sign is {context['zodiac']}")

    input = yield GetUserInput(message="What do you want to know?")
    yield User(content=input)

    value = yield Generate(settings={"temperature": 0.9})
    print(f"generated: {value}")

b = horoscope({"zodiac": "pisces"})

output, done = await run(b)
assert isinstance(output, GetUserInput)
assert not done

user_input = "Tell me my fortune"
output, done = await run(b, user_input)
assert isinstance(output, str)
assert done
```

![turbo](https://user-images.githubusercontent.com/931887/222912628-8662fad0-091f-4cb8-92f3-6cce287716e9.jpg)

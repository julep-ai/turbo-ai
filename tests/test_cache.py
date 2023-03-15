# flake8: noqa
from ward import test

from turbo_chat import *


@test("contains returns True when Generate no yield works")
async def test_turbo():
    cache = SimpleCache()

    @turbo(cache=cache)
    async def example():
        yield System(content="You are a good guy named John")
        yield User(content="What is your name?")
        result = yield Generate()

    b = example()
    results = [output async for output in b]

    assert len(cache.cache) == 1

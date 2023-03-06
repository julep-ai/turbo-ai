# flake8: noqa
from ward import test

from turbo_chat import *


@test("contains returns True when Generate no yield works")
async def test_turbo():
    @turbo()
    async def example(context={}):
        yield System(content="You are a good guy named John")
        yield User(content="What is your name?")
        result = yield Generate(yield_downstream=False)

        yield User(content="How are you doing?")
        result = yield Generate()

    b = example()
    results = [output async for output in b]

    assert len(results) == 1

# flake8: noqa
from ward import test

from turbo_chat import *


class TestMemory(LocalMemory):
    async def setup(self, hello: str):
        assert hello == "world"


@test("contains returns True when memory injection works")
async def test_memory_arg():
    @turbo(memory_class=TestMemory)
    async def example(zodiac: str, memory):
        yield System(content="You are a fortune teller")

    b = await example(zodiac="pisces", memory_args={"hello": "world"}).init()
    await b.run()

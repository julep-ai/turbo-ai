# flake8: noqa
from ward import test

from turbo_chat import *


class TestMemory(LocalMemory):
    async def setup(self, hello: str):
        assert hello == "world"


@test("contains returns True when memory injection works")
async def test_memory_arg():
    @turbo(memory_class=TestMemory)
    async def example():
        yield System(content="You are a fortune teller")

    await example(memory_args={"hello": "world"}).init()

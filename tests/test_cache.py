# flake8: noqa
from ward import test

from turbo_chat import *


@test("contains returns True when Generate no yield works")
async def test_cache():

    @turbo(cache_class=SimpleCache)
    async def example(cache):

        yield System(content="You are a good guy named John")
        yield User(content="What is your name?")
        
        assert len(cache.cache) == 1  # type: ignore

    b = example()
    await b.run()

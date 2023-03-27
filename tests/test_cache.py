# flake8: noqa
from ward import test

from turbo_chat import *


@test("contains returns True when Generate no yield works")
async def test_turbo():
    _cache = None

    @turbo(cache_class=SimpleCache)
    async def example(cache):
        nonlocal _cache
        _cache = cache

        yield System(content="You are a good guy named John")
        yield User(content="What is your name?")
        result = yield Generate()

    b = example()
    await b.init()

    results = [output async for output in b]

    assert len(_cache.cache) == 1  # type: ignore

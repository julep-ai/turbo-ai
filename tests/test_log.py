# flake8: noqa
from ward import test

from turbo_chat import *


@test("contains returns True when log fn is run correctly")
async def test_log():
    log_ran = False

    def log(message):
        nonlocal log_ran
        log_ran = True

    @turbo(log=log)
    async def example():
        yield Assistant(content="You are a fortune teller")

    await run(example())
    assert log_ran

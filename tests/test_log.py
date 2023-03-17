# flake8: noqa
from ward import test

from turbo_chat import *


@test("contains returns True when log fn is run correctly")
async def test_log():
    log_ran = False
    log_output = None

    def log(message):
        nonlocal log_ran
        nonlocal log_output

        log_ran = True
        log_output = message

    @turbo(log=log)
    async def example():
        yield Assistant(content="You are a fortune teller")

    await run(example())
    assert log_ran
    assert log_output and log_output["type"] == "output"

# flake8: noqa
from ward import test

from turbo_chat import *


@test("contains returns True when debug fn is run correctly")
async def test_debug():
    debug_ran = False
    debug_output = None

    def debug(message):
        nonlocal debug_ran
        nonlocal debug_output

        debug_ran = True
        debug_output = message

    @turbo(debug=debug)
    async def example():
        yield Assistant(content="You are a fortune teller")

    await run(example())
    assert debug_ran
    assert debug_output and debug_output["type"] == "output"

# flake8: noqa
from ward import test

from turbo_chat import *


@test("contains returns True when completion works")
async def test_completion_simple():
    name = "Baloo"

    @completion()
    async def say_hi(name: str):
        """Say hi to {{name}}"""

    assert name.lower() in (await say_hi(name=name)).lower()

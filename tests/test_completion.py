# flake8: noqa
from typing import TypedDict

from ward import test

from turbo_chat import *


@test("contains returns True when completion works")
async def test_completion_simple():
    name = "Baloo"

    @completion()
    async def say_hi(name: str):
        """Say hi to {{name}}"""

    assert name.lower() in (await say_hi(name=name)).lower()


@test("contains returns True when completion with parse works")
async def test_completion_parse():
    class Result(TypedDict):
        answer: str

    scratchpad: Scratchpad[Result] = Scratchpad(
        """
        Answer: {answer}
        """
    )

    @completion(parse=scratchpad.parse)
    async def what_is(concept: str):
        """
        Your response should start with `Answer:`.
        Question: What is {{concept}}?
        """

    concept = "apple"
    result: Result = await what_is(concept=concept)

    assert isinstance(result, dict)
    assert result["answer"]


@test("contains returns True when completion with positional args works")
async def test_completion_with_positional_args():
    name = "Baloo"

    @completion()
    async def say_hi(name: str):
        """Say hi to {{name}}"""

    assert name.lower() in (await say_hi(name)).lower()

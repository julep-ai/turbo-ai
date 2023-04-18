# flake8: noqa
from textwrap import dedent
from ward import test

from turbo_chat import *
from turbo_chat.apps import qa


@test("contains returns True when qa_bot works")
async def test_qa():
    context = 'User is a customer for "Julep Fashion Company" -- a company that sells fashion items and is asking the question to an online sales agent.'  # noqa: E501
    question = "What is the name of the company?"  # noqa: E501
    answer = await qa(context=context, question=question)

    assert isinstance(answer, Output)
    assert "julep" in answer.content.lower()

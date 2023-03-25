# flake8: noqa
from textwrap import dedent
from ward import test

from turbo_chat import *
from turbo_chat.bots import qa_bot


@test("contains returns True when qa_bot works")
async def test_qa_bot():
    context = 'User is a customer for "Julep Fashion Company" -- a company that sells fashion items and is asking the question to an online sales agent.'  # noqa: E501
    question = "What is the name of the company?"  # noqa: E501
    answer = await qa_bot(context=context, question=question).run()

    assert "julep" in answer.content.lower()

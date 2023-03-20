# flake8: noqa
from textwrap import dedent
from ward import test

from turbo_chat import *
from turbo_chat.bots import qa_bot, self_ask_bot


@test("contains returns True when self_ask_bot works")
async def test_self_ask_bot():
    context = "The best coat to buy is a Banana Twead Suit."  # noqa: E501
    subquery_instructions = 'User is a customer for "Julep Fashion Company" -- a company that sells fashion items and is asking the question to an online sales agent.'  # noqa: E501
    question = "What is the best suit to buy?"  # noqa: E501

    answer = await run(
        self_ask_bot(
            question=question,
            context=context,
            subquery_instructions=subquery_instructions,
            qa_bot=qa_bot,
        )
    )

    assert "banana" in answer.content.lower()

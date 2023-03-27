# flake8: noqa
from textwrap import dedent
from ward import test

from turbo_chat import *
from turbo_chat.bots import subqueries_bot


@test("contains returns True when subqueries_bot works")
async def test_subqueries_bot():
    context = 'User is a customer for "Julep Fashion Company" -- a company that sells fashion items and is asking the question to an online sales agent.'  # noqa: E501
    request = "Can you suggest me something to wear for my friend's wedding? I need something that's classy, black or beige and not too expensive."  # noqa: E501
    bot = await subqueries_bot(context=context, request=request).init()
    queries = await bot.run()

    assert isinstance(queries.content, list)
    assert 0 < len(queries.content)

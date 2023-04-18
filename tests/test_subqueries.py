# flake8: noqa
from textwrap import dedent
from ward import test

from turbo_chat import *
from turbo_chat.apps import subqueries


@test("contains returns True when subqueries works")
async def test_subqueries():
    context = 'User is a customer for "Julep Fashion Company" -- a company that sells fashion items and is asking the question to an online sales agent.'  # noqa: E501
    request = "Can you suggest me something to wear for my friend's wedding? I need something that's classy, black or beige and not too expensive."  # noqa: E501
    queries = await subqueries(context=context, request=request)

    assert isinstance(queries.content, list)
    assert 0 < len(queries.content)

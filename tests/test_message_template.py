# flake8: noqa
from ward import test

from turbo_chat import *


@test("contains returns True when message template works")
async def test_message_template():
    name = "Turbo"
    msg = Assistant(template="{{name}}", variables={"name": name})
    assert msg.content == name


@test("contains returns True when template validation works")
async def test_message_template():
    error_thrown = False

    try:
        msg = Assistant(
            template="{{name}}",
            variables={"gaga": "gaga"},
            check=True,
        )

    except:
        error_thrown = True

    assert error_thrown

# flake8: noqa
from ward import test

from turbo_chat import *


@test("contains returns True when message template works")
async def test_message_template():
    name = "Turbo"
    msg = Assistant(template="{{name}}", variables={"name": name})
    assert msg.content == name

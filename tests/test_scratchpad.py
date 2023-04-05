# flake8: noqa
from typing import Optional, TypedDict
from ward import test

from turbo_chat import *
from turbo_chat.bots.tool.scratchpad import scratchpad as tool_scratchpad


class ParsedSelfAskScratchpad(TypedDict):
    not_needed: Optional[str]
    follow_up_needed: Optional[bool]
    follow_up_question: Optional[str]
    final_response: Optional[str]
    explanation: Optional[str]


@test("contains returns True when scratchpad works")
async def test_scratchpad():
    spec = """
Not needed: {not_needed:S}
Are follow up questions needed here: {follow_up_needed:bool}
Follow up: {follow_up_question}
Final answer: {final_response:json}
Explanation: {explanation:multiline}
    """.strip()

    input = """
Random: blah
Are follow up questions needed here: yes
Follow up: gaga
Final answer: {gaga: "gaga"}
Explanation: this is a
multiline explanation
    """.strip()

    expected = {
        "follow_up_needed": True,
        "follow_up_question": "gaga",
        "final_response": {"gaga": "gaga"},
        "explanation": "this is a\nmultiline explanation",
    }

    scratchpad: Scratchpad[ParsedSelfAskScratchpad] = Scratchpad[
        ParsedSelfAskScratchpad
    ](spec)

    assert scratchpad.parse(input) == expected


@test("contains returns True when tool scratchpad works")
async def test_tool_scratchpad():
    input = """
Thought: Need to use a tool? Yes
Tool: SearchProducts
Tool Input: {"query": "wedding guest attire"}
""".strip()

    expected = {
        "tool_name": "SearchProducts",
        "tool_input": {"query": "wedding guest attire"},
    }

    assert tool_scratchpad.parse(input) == expected

@test("contains returns True when scratchpad json array works")
async def test_scratchpad_json_array():
    input = """
Input: [1, 2, 3]
"""
    
    scratchpad = Scratchpad(
"""
Input: {input:json}
""".strip()
    )

    expected = {
        "input": [1, 2, 3],
    }

    assert scratchpad.parse(input) == expected

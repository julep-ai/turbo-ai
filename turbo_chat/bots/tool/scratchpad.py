from typing import Optional, TypedDict

from ...structs import Scratchpad

__all__ = [
    "ParsedTools",
    "scratchpad",
]


class ParsedTools(TypedDict):
    should_use_tool: Optional[bool]
    tool_name: Optional[str]
    tool_input: Optional[dict]
    final_response: Optional[str]


scratchpad: Scratchpad[ParsedTools] = Scratchpad[ParsedTools](
    """
Tool: {tool_name:S}
Tool Input: {tool_input:json}
Response: {final_response}
""".strip()
)

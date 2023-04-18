from typing import cast, Generic, List, TypeVar

import dirtyjson
from parse import compile as compile_parser, Parser, with_pattern

__all__ = [
    "Scratchpad",
]

ST = TypeVar("ST")  # , bound=TypedDict) # Not available in py3.8

yesno_mapping = {
    "yes": True,
    "no": False,
    "on": True,
    "off": False,
    "true": True,
    "false": False,
    "1": True,
    "0": False,
}


@with_pattern(r"|".join(yesno_mapping))
def parse_yesno(text: str) -> bool:
    return yesno_mapping[text.lower()]


@with_pattern(r"([\[\{].+[\]\}])")
def parse_json(text: str) -> dict:
    return dirtyjson.loads(text)


@with_pattern(r".+")
def parse_multiline(text: str) -> str:
    return text


class Scratchpad(Generic[ST]):
    parsers: List[Parser]

    def __init__(self, spec: str):
        extra_types = dict(bool=parse_yesno, json=parse_json, multiline=parse_multiline)

        self.parsers = [
            compile_parser(
                spec_line + ("" if ":multiline" in spec_line else "\n"),
                extra_types=extra_types,
            )
            for spec_line in spec.strip().splitlines()
        ]

    def parse(self, input: str) -> ST:
        """Parse the input string according to the spec."""

        # Parse the scratchpad
        result = {}
        for parser in self.parsers:
            parsed = parser.search(input + "\n")
            result = {**result, **getattr(parsed, "named", {})}

        # Trim results
        result = {k: v.strip() if isinstance(v, str) else v for k, v in result.items()}

        return cast(ST, result)

from typing import cast, Generic, List, TypeVar

from parse import search as parse_search, with_pattern

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


class Scratchpad(Generic[ST]):
    def __init__(self, spec: str):
        self.spec = spec

    def _search(self, spec: str, input: str):
        """Use parse.search to parse scratchpad according to spec."""

        return parse_search(
            spec + "\n",
            input + "\n",
            extra_types=dict(bool=parse_yesno),
        )

    def parse(self, input: str) -> ST:
        """Parse the input string according to the spec."""
        """Only remembers latest results."""

        # Create parsers
        line_specs: List[str] = self.spec.split("\n")

        # Parse the scratchpad
        parsed = [self._search(spec, input) for spec in line_specs]

        # Collect results
        result = {}
        for parsed_line in parsed:
            p = parsed_line.named if parsed_line else {}
            result = {**result, **p}

        return cast(ST, result)

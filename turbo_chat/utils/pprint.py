from pprint import pformat
from typing import Any

from pygments import highlight
from pygments.formatters import Terminal256Formatter
from pygments.lexers import PythonLexer


def pprint_color(obj: Any) -> Any:
    """Pretty-print in color."""

    print(highlight(pformat(obj), PythonLexer(), Terminal256Formatter()), end="")
    return obj

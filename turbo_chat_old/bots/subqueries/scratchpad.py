from typing import Optional, TypedDict

from ...structs import Scratchpad

__all__ = [
    "ParsedQueries",
    "scratchpad",
]


class ParsedQueries(TypedDict):
    query1: Optional[str]
    query2: Optional[str]
    query3: Optional[str]
    query4: Optional[str]
    query5: Optional[str]
    query6: Optional[str]
    query7: Optional[str]
    query8: Optional[str]
    query9: Optional[str]
    query10: Optional[str]


scratchpad: Scratchpad[ParsedQueries] = Scratchpad[ParsedQueries](
    """
1. {query1}
2. {query2}
3. {query3}
4. {query4}
5. {query5}
6. {query6}
7. {query7}
8. {query8}
9. {query9}
10. {query10}
""".strip()
)

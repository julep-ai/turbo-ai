from typing import Any, List


class PickOptionalOff:
    pass


def pick(
    dictionary: dict,
    keys: List[str],
    optional: Any = PickOptionalOff(),
) -> dict:
    """Pick keys from dictionary and return as new dict."""

    return {
        key: (
            dictionary.get(key, optional)
            if isinstance(optional, PickOptionalOff)
            else dictionary[key]
        )
        for key in keys
    }

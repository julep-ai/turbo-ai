from typing import Callable, Set

import inspect
from inspect import Parameter as P


def get_required_args(fn: Callable) -> Set[str]:
    """Get required args for a function."""

    sig = inspect.signature(fn)
    params = list(sig.parameters.values())

    valid_param_kinds = [
        P.POSITIONAL_ONLY,
        P.POSITIONAL_OR_KEYWORD,
        P.KEYWORD_ONLY,
    ]

    required_params = [
        p.name for p in params if (p.default is p.empty and p.kind in valid_param_kinds)
    ]

    return set(required_params)


def ensure_args(fn: Callable, args: dict) -> bool:
    """Ensure that args dict has all required args for fn."""

    required_args: Set[str] = get_required_args(fn)
    required_intersection = required_args.intersection(set(args.keys()))
    has_all_required = required_intersection == required_args

    return has_all_required

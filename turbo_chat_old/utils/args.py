from typing import Callable, Set

import inspect
from inspect import Parameter as P


def get_fn_signature(fn: Callable) -> str:
    return ", ".join([str(p) for p in get_required_args(fn)])


def get_required_args(fn: Callable) -> list:
    """Get required args for a function."""

    sig = inspect.signature(fn)
    params = list(sig.parameters.values())

    valid_param_kinds = [
        P.POSITIONAL_ONLY,
        P.POSITIONAL_OR_KEYWORD,
        P.KEYWORD_ONLY,
    ]

    required_params = [
        p for p in params if (p.default is p.empty and p.kind in valid_param_kinds)
    ]

    return required_params


def ensure_args(fn: Callable, args: dict) -> bool:
    """Ensure that args dict has all required args for fn."""

    # Get required arg names for fn
    required_args: list = get_required_args(fn)
    required_args_set: Set[str] = set([p.name for p in required_args])

    # Get intersection of required args and args
    required_intersection = required_args_set.intersection(set(args.keys()))
    has_all_required = required_intersection == required_args_set

    return has_all_required

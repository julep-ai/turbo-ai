#!/usr/bin/env python3

from typing import List, Literal


__all__ = [
    "TurboModel",
    "available_models",
]

# Allowed chatgpt model names
TurboModel = Literal[
    "gpt-4",
    "gpt-4-0314",
    "gpt-4-32k",
    "gpt-4-32k-0314",
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-0301",
]

available_models: List[TurboModel] = [
    "gpt-4",
    "gpt-4-0314",
    "gpt-4-32k",
    "gpt-4-32k-0314",
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-0301",
]

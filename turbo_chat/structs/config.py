#!/usr/bin/env python3

from typing import Literal


__all__ = [
    "TurboModel",
]

# Allowed chatgpt model names
TurboModel = Literal[
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-0301",
]

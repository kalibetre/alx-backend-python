#!/usr/bin/env python3
"""
8-make_multiplier module
"""
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:

    def multiplier_func(num: float) -> float:
        return num * multiplier

    return multiplier_func

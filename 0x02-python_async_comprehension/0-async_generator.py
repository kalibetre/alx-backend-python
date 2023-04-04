#!/usr/bin/env python3
"""
0-async_generator module
"""
import asyncio
import random
from typing import Iterator


async def async_generator() -> Iterator[float]:
    """
    a simple async generator tha returns 10 random numbers between 0 and 10
    every second
    """
    for _ in range(10):
        await asyncio.sleep(1)
        yield random.uniform(0, 10)

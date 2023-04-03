#!/usr/bin/env python3
"""
1-concurrent_coroutines module
"""
import asyncio

wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> list:
    """
    returns the list of all the delays
    """
    c_routines = [wait_random(max_delay) for _ in range(n)]
    return [await delay for delay in asyncio.as_completed(c_routines)]

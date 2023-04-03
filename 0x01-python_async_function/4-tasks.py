#!/usr/bin/env python3
"""
4-tasks module
"""
import asyncio

task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> list:
    """
    returns the list of all delays in ascending order
    """
    c_routines = [task_wait_random(max_delay) for _ in range(n)]
    return [await delay for delay in asyncio.as_completed(c_routines)]

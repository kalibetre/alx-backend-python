#!/usr/bin/env python3
"""
2-measure_runtime module
"""
import asyncio
import time

async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime():
    """
    measures the total runtime required to run 4 async_comprehension calls
    """
    start = time.perf_counter()
    await asyncio.gather(*[async_comprehension() for _ in range(4)])
    end = time.perf_counter()
    return end - start

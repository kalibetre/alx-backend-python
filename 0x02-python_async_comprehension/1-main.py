#!/usr/bin/env python3
"""
0-main module
"""
import asyncio

async_comprehension = __import__('1-async_comprehension').async_comprehension


async def main():
    print(await async_comprehension())


asyncio.run(main())

# Task definitions

import asyncio

async def task_a():
    print("Running task A")
    await asyncio.sleep(1)
    return True

async def task_b():
    print("Running task B")
    await asyncio.sleep(1)
    return True

async def task_c():
    print("Running task C")
    await asyncio.sleep(1)
    return True

task_registry = {
    "task_a": task_a,
    "task_b": task_b,
    "task_c": task_c,
}

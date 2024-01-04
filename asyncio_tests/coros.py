import time
import asyncio

async def sleep_for(i):
    print(f'Starting time.sleep({i})', flush=True)
    time.sleep(i)
    print(f'Finished time.sleep({i})', flush=True)

async def asleep_for(i):
    print(f'Starting asyncio.sleep({i})', flush=True)
    await asyncio.sleep(i)
    print(f'Finished asyncio.sleep({i})', flush=True)


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)
    return delay 


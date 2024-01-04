"""
Experiments with asyncio
"""
import asyncio
import time

# this creates the coroutine
coro = sleep_for(1)

# this runs the coroutine
asyncio.run(coro)

coro = asleep_for(1)

asyncio.run(coro)


coros = [ asleep_for(i) for i in range(5) ]
asyncio.wait(coros)





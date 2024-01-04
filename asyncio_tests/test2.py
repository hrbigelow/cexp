import asyncio
from coros import asleep_for

coro = asleep_for(1)

task = asyncio.create_task(coro)
asyncio.run(task)

# loop = asyncio.get_event_loop()
# print(loop)



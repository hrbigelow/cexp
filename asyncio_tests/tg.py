import time
import asyncio
import coros

async def main():
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(coros.say_after(1, 'hello'))
        task2 = tg.create_task(coros.say_after(2, 'world'))
        print(f"started at {time.strftime('%X')}")
    # The await is implicit when the context manager exits.

    print(f"finished at {time.strftime('%X')}")
    for task in tg._tasks:
        result = await task
        print(result)


asyncio.run(main())


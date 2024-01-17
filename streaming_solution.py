from typing import List
import asyncio

def stream(streaming, seeds: List[int], lengths: List[int]) -> None:
    async def response(idx, sv, n):
        sv = sv % 10000 
        a, b = sv, sv 
        for _ in range(n):
            streaming.write_output(idx, a)
            a, b = b, (a + b) % 10000
            await asyncio.sleep(0)

    async def _run():
        async with asyncio.TaskGroup() as tg:
            for idx, (seed, length) in enumerate(zip(seeds, lengths)): 
                tg.create_task(response(idx, seed, length))
    asyncio.run(_run())


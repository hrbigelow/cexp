from typing import List
import asyncio

def stream(streaming, start_vals: List[int], lengths: List[int]) -> None:
    async def fibmod(idx, sv, rem, n):
        sv = sv % rem
        a, b = sv, sv 
        for _ in range(n):
            while a % 2 != 0:
                a, b = b, (a + b) % rem
            streaming.write_output(idx, a)
            await asyncio.sleep(0)

    mod_val = streaming.get_mod_val()

    async def _run():
        async with asyncio.TaskGroup() as tg:
            for idx, (start_val, length) in enumerate(zip(start_vals, lengths)): 
                tg.create_task(fibmod(idx, start_val, mod_val, length))
    asyncio.run(_run())


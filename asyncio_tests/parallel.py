"""
Launch with
export PYTHONPATH=/path/to/mymodule.cpython-311-x86_64-linux-gnu.so
python3 parallel.py ARGS
"""

from concurrent import futures
import sys
from functools import partial
import asyncio
from mymodule import intensive_calculation

async def sinsum_coro(i, n):
    print(f'Starting sinsum_coro({i}, {n})', flush=True)
    val = intensive_calculation(n)
    print(f'Finished sinsum_coro({i}, {n})', flush=True)
    return val

def sinsum(i, n):
    print(f'Starting sinsum({i}, {n})', flush=True)
    val = intensive_calculation(n)
    print(f'Finished sinsum({i}, {n})', flush=True)
    return val

async def main_task(n, p):
    """
    Run CPU-bound functions as tasks
    These all run in one OS thread on the same event loop
    """
    async with asyncio.TaskGroup() as tg:
        tasks = [ tg.create_task(sinsum_coro(i, n)) for i in range(p) ]

async def main_exec(n, p):
    """
    Run CPU-bound functions on a threadpool
    These tasks each run on different OS threads, and because they
    release the GIL, can actually achieve true parallelism (view with `top`)
    """
    loop = asyncio.get_running_loop()
    with futures.ThreadPoolExecutor() as pool:
        tasks = [loop.run_in_executor(pool, partial(sinsum, i, n)) for i in range(p)]
    # for task in tasks:
        # await task



if __name__ == '__main__':
    mode = sys.argv[1]
    n = int(float(sys.argv[2]))
    p = int(sys.argv[3])
    if mode == 'task':
        asyncio.run(main_task(n, p))
    elif mode == 'exec':
        asyncio.run(main_exec(n, p))



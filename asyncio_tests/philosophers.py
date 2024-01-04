"""
Define the Table class  
"""
import sys
import asyncio
import random
from concurrent import futures
from functools import partial

class Table:
    def __init__(self, n):
        self.n = n
        self.lock = asyncio.Lock()
        self.eating = [False] * n
        self.cond = [asyncio.Condition(self.lock) for _ in range(n)]
        self.num_eating = 0


    def _can_eat(self, i):
        return not (self.eating[(i-1)%self.n] or self.eating[(i+1)%self.n])

    def print(self):
        s = ''.join('-|'[e] for e in self.eating)
        print(f'{self.num_eating:3d} ' + s, flush=True)

    async def eat(self, i):
        async with self.cond[i]:
            await self.cond[i].wait_for(partial(self._can_eat, i))
            self.eating[i] = True
            self.num_eating += 1
            self.print()
        await asyncio.sleep(random.random())

    async def think(self, i):
        async with self.cond[i]:
            if self.eating[i]:
                self.num_eating -= 1
            self.eating[i] = False
            self.cond[(i-1)%self.n].notify()
            self.cond[(i+1)%self.n].notify()
            self.print()
        await asyncio.sleep(random.random())

    async def live(self, i):
        while True:
            await self.eat(i)
            await self.think(i)

async def main_tg(n):
    table = Table(n)
    async with asyncio.TaskGroup() as tg:
        tasks = [ tg.create_task(table.live(i)) for i in range(n) ]

if __name__ == '__main__':
    n = int(sys.argv[1])
    asyncio.run(main_tg(n))






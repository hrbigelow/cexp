"""
state: [is_eating] * n 
condition: [can_eat] * n
lock: protects all of state and conditions
"""
import asyncio
import time
import random
import threading
from concurrent import futures
from functools import partial
import sys

class Table:
    def __init__(self, n):
        # create a table with n philosophers
        self.n = n
        self.lock = threading.Lock()
        self.eating = [False] * n # initially, no philosophers are eating
        self.cond = [threading.Condition(self.lock) for _ in range(n)]
        self.num_eating = 0

    def eat(self, i):
        # i'th philosopher eats
        with self.cond[i]:
            while self.eating[(i-1)%self.n] or self.eating[(i+1)%self.n]:
                self.cond[i].wait()
            self.eating[i] = True
            self.num_eating += 1
            # self.cond[i].notify()
            s = ''.join('-|'[e] for e in self.eating)
            print(f'{self.num_eating:3d} ' + s, flush=True)
        time.sleep(random.random())

    def think(self, i):
        with self.cond[i]:
            if self.eating[i]:
                self.num_eating -= 1
            self.eating[i] = False
            self.cond[(i-1)%self.n].notify()
            self.cond[(i+1)%self.n].notify()
            s = ''.join('-|'[e] for e in self.eating)
            print(f'{self.num_eating:3d} ' + s, flush=True)
        time.sleep(random.random())

    def live(self, i):
        while True:
            self.think(i)
            self.eat(i)

def main(n):
    table = Table(n)
    threads = [threading.Thread(target=table.live, args=(i,)) for i in range(n)]
    for th in threads:
        th.start()
    # for th in threads:
        # th.join()

async def main_executor(n):
    table = Table(n)
    loop = asyncio.get_running_loop()
    with futures.ThreadPoolExecutor(max_workers=n//2) as pool:
        results = [ loop.run_in_executor(pool, partial(table.live, i)) for i in range(n) ]
        # for result in results:
            # await result

if __name__ == '__main__':
    n = int(sys.argv[1])
    # main(n)
    asyncio.run(main_executor(n))


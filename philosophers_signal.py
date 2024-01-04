import threading
import time
import random

class Philosopher(threading.Thread):
    def __init__(self, i, table):
        super().__init__(target=self.run)
        self.idx = i
        self.eating = False
        self.table = table
        self.condition = threading.Condition(table)
        self.rand = random.Random()

    def set_left(self, left):
        self.left = left

    def set_right(self, right):
        self.right = right

    def run(self):
        try:
            while True:
                self.think()
                self.eat()
        except KeyboardInterrupt:
            raise

    def think(self):
        with self.condition:
            self.eating = False
            self.left.condition.notify()
            self.right.condition.notify()
            print(' ' * self.idx + 'T', flush=True)
        time.sleep(self.rand.uniform(0, 1))

    def eat(self):
        with self.condition:
            # while self.left.eating or self.right.eating:
            while self.left.eating or self.right.eating:
                self.condition.wait()
            self.eating = True
            print(' ' * self.idx + 'E', flush=True)
        time.sleep(self.rand.uniform(0, 5))

def main(n):
    table = threading.Lock()
    philosophers = [ Philosopher(i, table) for i in range(1, n+1) ]
    for i in range(n):
        philosophers[i].set_left(philosophers[(i-1)%n])
        philosophers[i].set_right(philosophers[(i+1)%n])
    
    for i in range(n):
        philosophers[i].start()

if __name__ == '__main__':
    main(10)

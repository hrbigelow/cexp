import sys
import threading

"""
Condition where a thread should wake up:

step > n or cond

Condition where the thread should sleep:

not (step > n or cond)
not step > n and not cond
"""

class FizzBuzz:
    def __init__(self, n: int):
        self.n = n
        # protects i
        self.cond = threading.Condition()
        self._step = 1

    def _is(self, kind):
        val = self._step
        if kind == 'fizz':
            return val % 3 == 0 and val % 5 != 0
        elif kind == 'buzz':
            return val % 5 == 0 and val % 3 != 0
        elif kind == 'fizzbuzz':
            return val % 15 == 0
        else: # kind == 'number'
            return val % 3 != 0 and val % 5 != 0

    # printFizz() outputs "fizz"
    def fizz(self, printFizz: 'Callable[[], None]') -> None:
        with self.cond:
            while True:
                while self._step <= self.n and not self._is('fizz'):
                    self.cond.wait()
                if self._step > self.n:
                    break
                printFizz()
                self._step += 1
                self.cond.notify_all()
            self.cond.notify_all()

    # printBuzz() outputs "buzz"
    def buzz(self, printBuzz: 'Callable[[], None]') -> None:
        with self.cond:
            while True:
                while self._step <= self.n and not self._is('buzz'):
                    self.cond.wait()
                if self._step > self.n:
                    break
                printBuzz()
                self._step += 1
                self.cond.notify_all()
            self.cond.notify_all()
    	

    # printFizzBuzz() outputs "fizzbuzz"
    def fizzbuzz(self, printFizzBuzz: 'Callable[[], None]') -> None:
        with self.cond:
            while True:
                while self._step <= self.n and not self._is('fizzbuzz'):
                    self.cond.wait()
                if self._step > self.n:
                    break
                printFizzBuzz()
                self._step += 1
                self.cond.notify_all()
            self.cond.notify_all()
        

    # printNumber(x) outputs "x", where x is an integer.
    def number(self, printNumber: 'Callable[[int], None]') -> None:
        with self.cond:
            while True:
                while self._step <= self.n and not self._is('number'):
                    self.cond.wait()
                if self._step > self.n:
                    break
                printNumber(self._step)
                self._step += 1
                self.cond.notify_all()
            self.cond.notify_all()
        

def printFizz():
    print('fizz', flush=True)

def printBuzz():
    print('buzz', flush=True)

def printFizzBuzz():
    print('fizzbuzz', flush=True)

def printNumber(i):
    print(i, flush=True)

def main(n):
    fb = FizzBuzz(n)
    t1 = threading.Thread(target=fb.fizz, args=(printFizz,))
    t2 = threading.Thread(target=fb.buzz, args=(printBuzz,))
    t3 = threading.Thread(target=fb.fizzbuzz, args=(printFizzBuzz,))
    t4 = threading.Thread(target=fb.number, args=(printNumber,))

    t1.start()
    t2.start()
    t3.start()
    t4.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()
    print('Finished')

if __name__ == '__main__':
    n = int(sys.argv[1])
    main(n)


import sys
import threading

class FizzBuzz:
    def __init__(self, n: int):
        self.n = n
        self.i = 1 # state
        self.cond = threading.Condition()

    @staticmethod
    def _is_fizz(i):
        return i % 3 == 0 and i % 5 != 0

    @staticmethod
    def _is_buzz(i):
        return i % 3 != 0 and i % 5 == 0

    @staticmethod
    def _is_fizzbuzz(i):
        return i % 15 == 0

    @staticmethod
    def _is_number(i):
        return i % 3 != 0 and i % 5 != 0

    # printFizz() outputs "fizz"
    def fizz(self, printFizz: 'Callable[[], None]') -> None:
        with self.cond:
            while self.i <= self.n:
                while self.i <= self.n and not self._is_fizz(self.i):
                    # print(f'waiting on {self.i}', flush=True)
                    self.cond.wait()
                # if self.i > self.n:
                    # break
                if self._is_fizz(self.i):
                    printFizz()
                    self.i += 1
                    self.cond.notify_all()

    # printBuzz() outputs "buzz"
    def buzz(self, printBuzz: 'Callable[[], None]') -> None:
        with self.cond:
            while self.i <= self.n:
                while self.i <= self.n and not self._is_buzz(self.i):
                    # print(f'waiting on {self.i}', flush=True)
                    self.cond.wait()
                # if self.i > self.n:
                 #    break
                if self._is_buzz(self.i):
                    printBuzz()
                    self.i += 1
                    self.cond.notify_all()

    # printFizzBuzz() outputs "fizzbuzz"
    def fizzbuzz(self, printFizzBuzz: 'Callable[[], None]') -> None:
        with self.cond:
            while self.i <= self.n:
                while self.i <= self.n and not self._is_fizzbuzz(self.i):
                    # print(f'waiting on {self.i}', flush=True)
                    self.cond.wait()
                # if self.i > self.n:
                    # break
                if self._is_fizzbuzz(self.i):
                    printFizzBuzz()
                    self.i += 1
                    self.cond.notify_all()

    # printNumber(x) outputs "x", where x is an integer.
    def number(self, printNumber: 'Callable[[int], None]') -> None:
        with self.cond:
            while self.i <= self.n:
                while self.i <= self.n and not self._is_number(self.i):
                # while not self._is_number(self.i):
                    # print(f'waiting on {self.i}', flush=True)
                    self.cond.wait()
                if self._is_number(self.i):
                    printNumber(self.i)
                    self.i += 1
                    # self.cond.notify_all()
                    self.cond.notify()

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



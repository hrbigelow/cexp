"""
Four theads, each one calls one of the below functions *once*
I like the shared data approach, with each thread incrementing a shared state
of 'i'

"""
import sys
import threading

class FizzBuzz:
    def __init__(self, n: int):
        self.n = n+1
        self.step = 0
        self.cond = threading.Condition()

    def _loop(self, pred, fn, call_with_step=False):
        with self.cond:
            while True:
                self.cond.wait_for(lambda: self.step == self.n or pred())
                if self.step == self.n:
                    break
                args = (self.step,) if call_with_step else ()
                # print(f'{self.step=}, {fn=}', flush=True)
                fn(*args)
                self.step += 1
                # print(self.step)
                self.cond.notify_all()
            self.cond.notify_all()

    def _kind(self, kind):
        if self.step % 3 == 0:
            if self.step % 5 == 0:
                return kind == 'fizzbuzz'
            else:
                return kind == 'fizz'
        else:
            if self.step % 5 == 0:
                return kind == 'buzz'
            else:
                return kind == 'number'


    # printFizz() outputs "fizz"
    def fizz(self, printFizz: 'Callable[[], None]') -> None:
        self._loop(lambda: self._kind('fizz'), printFizz)

    # printBuzz() outputs "buzz"
    def buzz(self, printBuzz: 'Callable[[], None]') -> None:
        self._loop(lambda: self._kind('buzz'), printBuzz)
    	
    # printFizzBuzz() outputs "fizzbuzz"
    def fizzbuzz(self, printFizzBuzz: 'Callable[[], None]') -> None:
        self._loop(lambda: self._kind('fizzbuzz'), printFizzBuzz)

    # printNumber(x) outputs "x", where x is an integer.
    def number(self, printNumber: 'Callable[[int], None]') -> None:
        self._loop(lambda: self._kind('number'), printNumber, True)
        
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


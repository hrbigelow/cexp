"""
The following problem concerns concurrent generation of N individual modified
fibonacci sequences.  The goal is to generate the elements of each sequence as
intercalated as possible, as you might if these were N ChatGPT responses being
streamed to individual users, and you want each new element to appear roughly at the
same rate.

Let fibmod(start, remval, i) be the "i'th modded, even fibonacci number starting at
`start`", as defined below:

fib(1,:)         = 1 1 2 3 5 8 13 21 34 55 89
fib(1,:) % 10    = 1 1 3 4 5 8 3 1 4 5 9 ...
fibmod(1, 10, :) = 4 8 4 ...

Think of the `fibmod` function as a stand-in for some ongoing task or process which
has its own independent dynamics and must be progressively computed, and periodically
produce output. 

You are given the following API functions:

get_mod_val() -> int

write_output(idx, val) -> None

Both functions record the timestamp when they are called.  You must implement a
function that produces the same sequence of calls to `write_output` as defined by the 
`stream` function below.  `fibmod` is not provided.

In addition to producing the correct sequence of `write_output` calls, you should
attempt to:

1. minimize the time gap between the first `get_mod_val()` call and the first
`write_output` call.  (That precludes trying to pre-compute all of the `write_output`
data before actually calling `write_output`)

2. strive to minimize the maximal time interval between any two adjacent calls of
`write_output` with the same index.


"""
from typing import List
import random
import time
import sys

class Streaming:
    def __init__(self, start_vals, lengths):
        self.mod_val = None
        self.timestamps = []
        self.indexes = []
        self.fibmods = []
        self.start_vals = start_vals
        self.lengths = lengths
        self.n = len(self.start_vals)

    def get_mod_val(self):
        start = time.monotonic()
        self.timestamps.append(start)
        self.indexes.append(None)
        self.fibmods.append(None)
        self.mod_val = random.choice(range(10000, 50000))
        return self.mod_val

    def write_output(self, idx, val):
        self.timestamps.append(time.monotonic())
        self.indexes.append(idx)
        self.fibmods.append(val)

    def _fibmod(self, idx):
        # yield the even subset of the modded fibonacci starting at `start`
        start = self.start_vals[idx] % self.mod_val
        n = self.lengths[idx]
        a, b = start, start
        for _ in range(n):
            while a % 2 != 0:
                a, b = b, (a + b) % self.mod_val
            yield a 

    def check_order(self):
        # Call after user calls stream to confirm correctness
        gens = [self._fibmod(idx) for idx in range(self.n)]
        z = zip(self.indexes, self.fibmods)
        next(z) # throw away first value
        for idx, val in z:
            try:
                uval = next(gens[idx])
            except:
                return False
            if val != uval:
                return False
        return True

    def find_max_gap(self):
        # Find maximum time gap in each stream between consecutive outputs 
        prev_time = [None] * self.n
        max_gaps = [0] * self.n
        z = zip(self.indexes, self.timestamps)
        next(z) # throw away first value
        for idx, ts in z:
            if prev_time[idx] is not None:
                max_gaps[idx] = max(max_gaps[idx], ts - prev_time[idx])
            prev_time[idx] = ts
        return max(max_gaps)

def stream(streaming: Streaming, start_vals: List[int], lengths: List[int]) -> None:
    """
    The user-provided function.
    This function must call streaming.get_mod_val(), and then call
    streaming.write_output() repeatedly to generate the intercalated sequences.
    """
    raise NotImplementedError

def evaluate(n, stream_fn):
    """
    Evaluate user-provided `stream_fn` on `n` concurrent streams.
    Signature:
    stream_fn(streaming: Streaming, start_vals: List[int], lengths: List[int]) -> None
    """
    start_vals = random.choices(range(50000), k=n)
    lengths = random.choices(range(1000, 2000), k=n)
    streaming = Streaming(start_vals, lengths)
    stream_fn(streaming, start_vals, lengths)
    print(f'{len(streaming.fibmods)=}')
    if not streaming.check_order():
        print(f'Failed ordering check')
        return False
    max_time_lag = streaming.find_max_gap()
    print(f'Maximun time lag: {max_time_lag:0.5f}')


if __name__ == '__main__':
    n = int(sys.argv[1])
    evaluate(n, stream)



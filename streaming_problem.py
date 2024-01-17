# Run with e.g.:
# cd to the directory containing cexp
# python -m cexp.streaming_problem 100

"""
A server must concurrently stream responses for N users' queries.  A response
consists of a sequence of integers sent to a user.  The sequence is defined by
pseudo-code: 

response(seed, mod, length):
    a, b = seed, seed
    for _ in range(length):
        a, b = b, (a + b) % mod
        yield a

The server sends each integer one at a time to a given user using an API call.  The
user sees the integer appear on his screen in real time.  In order to provide the
nicest user experience, the goal is to send the integers as fast as possible, but at
a rate as evenly as possible for each user.

You are given the following API functions:

get_mod() -> int
# returns the mod value to use for all responses

write_output(idx, val) -> None
# called to generate one element `val` of response `idx`

You must implement a function with the following signature:

stream(seeds: List[int], lengths: List[int]) -> None

The `stream` function first calls `get_mod()` to get the mod value.  Then it must
call `write_output` lengths[idx] times for each idx.  The values must be consistent
with the response sequence as defined by `response(seeds[idx], mod, lengths[idx])`

Additionally, all calls to `get_mod()` and `write_output` have a timestamp recorded.
Once all responses are completed, the maximum step duration is computed.  This is the
maximum time lag between any two elements within a response.

Constraints:

10 <= N <= 100000
len(seeds) == N
len(length) == N
1 <= seeds[i] <= 1000
10000 <= mod <= 20000
1000 <= length[i] <= 2000

"""

from .streaming_solution import stream
from typing import List
import random
import time
import sys


class Server:
    """
    Class providing backend framework for generating test cases and validation
    User must provide the `stream` function
    """
    def __init__(self, seeds, lengths):
        self.mod_val = None
        self.timestamps = []
        self.indexes = []
        self.values = []
        self.seeds = seeds
        self.lengths = lengths
        self.n = len(self.seeds)

    def get_mod_val(self):
        start = time.monotonic()
        self.timestamps.append(start)
        self.indexes.append(None)
        self.values.append(None)
        self.mod_val = random.choice(range(10000, 50000))
        return self.mod_val

    def write_output(self, idx, val):
        self.timestamps.append(time.monotonic())
        self.indexes.append(idx)
        self.values.append(val)

    def _response(self, idx):
        # yields the response for user `idx` 
        start = self.seeds[idx] % self.mod_val
        n = self.lengths[idx]
        a, b = start, start
        for _ in range(n):
            yield a 
            a, b = b, (a + b) % self.mod_val

    def check_order(self):
        # Call after user calls stream to confirm correctness
        gens = [self._response(idx) for idx in range(self.n)]
        z = zip(self.indexes, self.values)
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

    def evaluate(self, stream_fn):
        """
        Evaluate user-provided `stream_fn` on `n` concurrent streams.
        Signature:
        stream_fn(streaming: Streaming, seeds: List[int], lengths: List[int]) -> None
        """
        stream_fn(self, self.seeds, self.lengths)
        if not self.check_order():
            print(f'Failed ordering check')
            return False
        max_time_lag = self.find_max_gap()
        print(f'Maximun time lag: {max_time_lag:0.5f}')



# def stream(server: Server, seeds: List[int], lengths: List[int]) -> None:
    """
    The user-provided function.
    This function must call streaming.get_mod_val(), and then call
    streaming.write_output() repeatedly to generate the intercalated sequences.
    """

def main(n):
    seeds = random.choices(range(50000), k=n)
    lengths = random.choices(range(1000, 2000), k=n)
    server = Server(seeds, lengths)
    server.evaluate(stream)

if __name__ == '__main__':
    n = int(sys.argv[1])
    main(n)



# How to run:
# git clone https://github.com/hrbigelow/cexp.git
# python -m cexp.streaming_problem <n>
# This will run a test case with concurrency level n (10000 takes several seconds)
# To try your own solution, uncomment the `stream` function below

"""
A server must concurrently stream responses for N users' queries.  A response
consists of a sequence of integers sent to a user.  The sequence is defined by
pseudo-code: 

response(seed, length):
    a, b = seed, seed
    for _ in range(length):
        a, b = b, (a + b) % 10000
        yield a

The server sends each integer one at a time to a given user using an API call.  The
user sees the integer appear on his screen in real time.  In order to provide the
nicest user experience, the goal is to send the integers as fast as possible, but at
a rate as evenly as possible for each user.  Additionally, the time from program
start to appearance of the first integer should be minimized.  

You are given the following API function:

write_output(idx, val) -> None
# called to generate one element `val` of response `idx`
# records current time when called

You must implement a function with the following signature:

stream(seeds: List[int], lengths: List[int]) -> None

The stream function must generate the server responses by repeatedly calling
`write_output(idx, val)` such that each subsequence for a given `idx` corresponds to
`response(seeds[idx], lengths[idx])`.

Temporal User Experience Scores

For user `idx`, two scores will be used to quantify the temporal quality of
the user's experience, as defined by Server.temporal_scores 

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
        self.launch_time = time.monotonic()
        self.timestamps = []
        self.indexes = []
        self.values = []
        self.seeds = seeds
        self.lengths = lengths
        self.n = len(self.seeds)

    def write_output(self, idx, val):
        self.timestamps.append(time.monotonic())
        self.indexes.append(idx)
        self.values.append(val)

    def _response(self, idx):
        # yields the response for user `idx` 
        start = self.seeds[idx] % 10000
        n = self.lengths[idx]
        a, b = start, start
        for _ in range(n):
            yield a 
            a, b = b, (a + b) % 10000 

    def check_order(self):
        # Call after user calls stream to confirm correctness
        gens = [self._response(idx) for idx in range(self.n)]
        z = zip(self.indexes, self.values)
        for idx, val in z:
            try:
                uval = next(gens[idx])
            except:
                return False
            if val != uval:
                return False
        return True

    def _decollate(self):
        timestamps = [list() for _ in range(self.n)]
        for idx, ts in zip(self.indexes, self.timestamps):
            timestamps[idx].append(ts)
        return timestamps 

    def temporal_scores(self):
        # computes the maximal initial_lag, rate_variation across all users
        timestamps = self._decollate()
        max_variation = 0
        max_lag = 0
        for ts in timestamps:
            jank = max(b-a for a,b in zip(ts[:-1], ts[1:]))
            span = ts[-1] - ts[0]
            lag = (ts[0] - self.launch_time) / span
            max_lag = max(max_lag, lag)
            max_variation = max(max_variation, jank / span)
        return max_lag, max_variation

    def evaluate(self, stream_fn):
        """
        Calls `stream_fn`, then evaluates correctness and temporal scores.
        Signature: stream_fn(server: Server, seeds: List[int], lengths: List[int]) -> None
        """
        stream_fn(self, self.seeds, self.lengths)
        if not self.check_order():
            print(f'Failed ordering check')
            return False
        max_lag, max_variation = self.temporal_scores()
        print(f'Max start lag: {max_lag:0.5f}')
        print(f'Max variation: {max_variation:0.5f}')

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



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

def stream(start_vals: List[int], lengths: List[int]) -> None:
    # pseudo-code
    mod_val = get_mod_val() # This starts the timer!
    for i in range(max(lengths)):
        for idx, start_val in enumerate(start_vals):
            if i < lengths[idx]:
                write_output(idx, fibmod(start_val, mod_val, i))

        
   
    


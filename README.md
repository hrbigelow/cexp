# Concurrency Experiments

## Python threads that release GIL can run on multiple cores

    python3 parallel_threads.py

What might be happening:
Shows 600% CPU utilization with top (on my 6-core laptop).  The `ThreadPoolExecutor`
launches 6 threads.  Initially, only one can run since it holds the GIL.  When it
enters the C portion and releases the GIL (see mymodule.pyx:9) *somehow* the Python
interpreter thread knows this, and elects for another suspended thread to acquire the
GIL and resume.  However, because there are 6 cores on the machine, the resuming of
the second thread has a separate core available to it, so the kernel need not preempt
the first thread.  The second thread resumes on a separate core and enters the nogil
region (releases the GIL).  The Python interpreter thread is notified, chooses one of
the four remaining suspended threads and gives it the GIL and the process repeats.

Setting `sys.setswitchinterval()` to values 0.05, 1.0 or 10.0 have no effect on the
total wall clock time of `parallel_threads.py`.  It could be that the waking up of
each thread happens immediately as the previous thread enters the nogil state - that
would be possible if the python interpreter was notified and in turn notified the
next suspended thread.


## A time.busy would be nice

`time.sleep(s)` actually causes a thread to be *suspended* for `s` seconds.  When you
are trying to reason about concurrency and parallelism and CPU usage, it is incorrect
to use `time.sleep(s)` to try to simulate the thread doing `s` seconds of work.  But,
as far as I know, there is no generic function (in python or C) that does the
equivalent of 'be busy for s seconds'.  Such a function would be very useful in
trying to reason about workloads because it would simulate what we actually want.



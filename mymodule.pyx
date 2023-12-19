from libc.math cimport sin
from cython.parallel import prange

def intensive_calculation(int n):
    cdef double result = 0
    cdef int i
    # Releasing the GIL
    with nogil:
        for i in prange(n, schedule='guided'):
            result += sin(i)
    return result


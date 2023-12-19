# To install mymodule run:
# python setup.py build_ext --inplace
import sys

sys.setswitchinterval(0.05)

from mymodule import intensive_calculation 
from concurrent import futures

# top shows 600% CPU while this runs
with futures.ThreadPoolExecutor() as executor:
    res = executor.map(intensive_calculation, [200000000] * 6)



"""
Python sys module and usage
"""

import sys

from icecream import ic

temp = [1, 2, 3]

# Returns memory size in btes
ic(sys.getsizeof(temp))
temp_int = 8
ic(sys.getsizeof(temp_int))

# Returns the list of command line arguments
print(sys.argv)


# Returns python path

print(sys.path)

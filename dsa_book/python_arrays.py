from array import array
from ctypes import Array
from sys import getsizeof

from icecream import ic

foo_arr = array("i", [1, 2, 3])
ic(foo_arr)
ic(getsizeof(foo_arr[0]) + getsizeof(foo_arr[0]) + getsizeof(foo_arr[0]))
ic(getsizeof(foo_arr))
ic(type(foo_arr))
ic([id(i) for i in foo_arr])

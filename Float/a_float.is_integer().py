from icecream import ic
a_float = 56.44
b_float = 56.00
ic(a_float.is_integer())  # the float value of a_float is not integer thus returns False
ic(b_float.is_integer())  # the float value of b_float is integer thus returns True
#op: ic| a_float.is_integer(): False
#op: ic| b_float.is_integer(): True

#%%
from icecream import ic
# vowels list
py_list = ['e', 'a', 'u', 'o', 'i']
ic(sorted(py_list))
ic(py_list)
#op:  sorted(py_list): ['a', 'e', 'i', 'o', 'u']
#op: py_list: ['e', 'a', 'u', 'o', 'i']
#%%
# string
py_string = 'Python'
ic(sorted(py_string))
#op: sorted(py_string): ['P', 'h', 'n', 'o', 't', 'y']
#%%
# vowels tuple
py_tuple = ('e', 'a', 'u', 'o', 'i')
ic(sorted(py_tuple))
#op: sorted(py_tuple): ['a', 'e', 'i', 'o', 'u']

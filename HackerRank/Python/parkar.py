from itertools import permutations
from collections import Counter
seq = permutations(['a','b','b'])
for each in seq:
    print("".join(each))
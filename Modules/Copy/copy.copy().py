"""using copy module"""
import copy
x = {"a": 3, "b": 5, "c": [1, 2, [1, {"z": 3}]]}
y = x.copy()
print(x)
print(y)

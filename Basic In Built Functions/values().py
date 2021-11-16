my_dict = {"a": 4, "b": 5, "c": 45}
print(my_dict)
item=[]
item = my_dict.items()  # returns the keys in the dictionary
print(item)
print(type(item))
#  >> {'a': 4, 'b': 5, 'c': 45}
#     dict_items([('a', 4), ('b', 5), ('c', 45)])
#     <<class 'dict_items'>

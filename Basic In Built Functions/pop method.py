a_list = ["cat", "dog", "tiger"]
a_list.pop(1)  # Removes the contents at index location 1
print(a_list)
# >>['cat', 'tiger']

#  to return a popped item
a_list = ["cat", "dog", "tiger"]
popped_item = a_list.pop(1)  # Removes the contents at index location 1 and returns the popped
# value
print(a_list)
print(popped_item)
# >>['cat', 'tiger']
# >>dog

#pop without index specified
a_list = ["cat", "dog", "tiger"]
a_list.pop()  # Removes the contents at index location -1(last item
print(a_list)
# >>['cat', 'dog']

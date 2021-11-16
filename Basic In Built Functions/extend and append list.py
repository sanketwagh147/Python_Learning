first_list = [1, 2, 3]
second_list = [4, 5, 6]
first_list.append(second_list)  # This does not return anything
print(first_list)
# >>[1, 2, 3, [4, 5, 6]]

# Reset list and use extend
first_list = [1, 2, 3]
second_list = [4, 5, 6]
first_list.extend(second_list)
print(first_list)
#  >>[1, 2, 3, 4, 5, 6]

# Reset list and use + instead of extend
first_list = [1, 2, 3]
second_list = [4, 5, 6, 9]
third_list = first_list+second_list
print(third_list)


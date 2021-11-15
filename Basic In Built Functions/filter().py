# # find even list
a_list = list(range(0,17))
print(a_list)
# even_list = list(filter(lambda x: x % 2 == 0, a_list))
# print(even_list)
perfect_square = list(filter(lambda x:(x**0.5).is_integer(), a_list))
print(perfect_square)

# # to filter empty string in a given list
# str_list =["kanda", "batab", "", "djkjk", "", " hajdh"]
# remove_empty_string_list = list(filter(None, str_list))
# print(remove_empty_string_list)
#
# # to filter int(0) in a given list




















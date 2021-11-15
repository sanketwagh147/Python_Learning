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
# int_list = [1, 3, 4, 0, 123, 99, 0, 123, 123, 998, 88]
# remove_empty_0_list = list(filter(None, int_list))
# print(remove_empty_0_list)
#
# #usig filter and list comprehesions

# a_string = " This is so crazy I am going to use string comprehension a a string into list wiht each individual items filtering empty values"
#
# dubu2 = [i for i in a_string]
# dubu3 = list(filter(None, dubu2))

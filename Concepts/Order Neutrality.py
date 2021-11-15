"""order neutrality sets are order neutral while list are not"""
a_list = [1, 2, 3]  # both sets have same but the order are different
b_list = [1, 3, 2]
a_set = [1, 3, 2]  # both sets have same item but order is different
b_set = [1, 3, 2]

list_equal = a_list == b_list
print(list_equal)
#op: False
set_equal = a_set == b_set
print(set_equal)
#op: True

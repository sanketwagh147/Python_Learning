#%% code to create random lists of strings and integers
import string
import random
str_list = []
no_of_items_on_list = 5
no_of_characters_in_each_string_in_list = 5
letters = string.ascii_letters
while no_of_items_on_list > 0:
    str_list.append(''.join(random.choice(letters) for i in range(no_of_characters_in_each_string_in_list)))
    no_of_items_on_list -= 1

no_of_items_on_list = 5
print(str_list)
#op:['dUcXr', 'HbFKf', 'RiPsg', 'Btdqs', 'eiQAg']
int_list = list(range(0, no_of_items_on_list))
print(int_list)
#op:[0, 1, 2, 3, 4]
#%%
use_of_zip = (zip(int_list, str_list))  # This will create a tuple iterating both iterable if one has less value then the length
#Will be based on length of smallest iterable

zipped_list = list(use_of_zip)
print(zipped_list)
#op:[(0, 'dUcXr'), (1, 'HbFKf'), (2, 'RiPsg'), (3, 'Btdqs'), (4, 'eiQAg')]
#%%
use_of_zip = (zip(int_list, str_list, ("boo", "boo")))  # If one has less value then the length Will be based on length of smallest iterable
zipped_list = list(use_of_zip)
print(zipped_list)
#op: [(0, 'dUcXr', 'boo'), (1, 'HbFKf', 'boo')]

import string
import random
str_list = []
no_of_items_on_list = 5
no_of_characters_in_each_string_in_list = 5
letters = string.ascii_lowercase
while no_of_items_on_list > 0:
    str_list.append(''.join(random.choice(letters) for i in range(no_of_characters_in_each_string_in_list)))
    no_of_items_on_list -=1

print(str_list)

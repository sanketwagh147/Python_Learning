import string
import random
str_list = []
no_of_items_on_list = 5
no_of_characters_in_each_string_in_list = 5
letters = string.ascii_letters
while no_of_items_on_list > 0:
    str_list.append(''.join(random.choice(letters) for i in range(no_of_characters_in_each_string_in_list)))
    no_of_items_on_list -=1

no_of_items_on_list = 5
print(str_list)
int_list = list(range(0, no_of_items_on_list))
print(int_list)

use_of_zip = (zip(int_list, str_list))  #This will create a tuple iterating both iterable if one has less value then the lenght
                                        #Will be based on lenght of smallest iterable

zipped_list = list(use_of_zip)
print(zipped_list)

use_of_zip = (zip(int_list, str_list,("boo", "boo")))  #This will create a tuple iterating both iterable if one has less value then the length
                                        #Will be based on lenght of smallest iterable

zipped_list = list(use_of_zip)
print(zipped_list)

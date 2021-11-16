#Write a function called modify_dict. modify_dict takes one
#parameter, a dictionary. The dictionary's keys are people's
#last names, and the dictionary's values are people's first
#names. For example, the key "Joyner" would have the value
#"David".
#
#modify_dict should delete any key-value pair for which the
#key's first letter is not capitalized. For example, the
#key-value pair "joyner":"David" would be deleted, but the
#key-value pair "Joyner":"david" would not be deleted. Then,
#return the modified dictionary.
#
#Remember, the keyword del deletes items from lists and
#dictionaries. For example, to remove the key "key!" from
#the dictionary my_dict, you would write: del my_dict["key!"]
#Or, if the key was the variable my_key, you would write:
#del my_dict[my_key]
#
#Hint: If you try to delete items from the dictionary while
#looping through the dictionary, you'll run into problems!
#We should never change the number if items in a list or
#dictionary while looping through those items. Think about
#what you could do to keep track of which keys should be
#deleted so you can delete them after the loop is done.
#
#Hint 2: To check if the first letter of a string is a
#capital letter, use string[0].isupper().


#Write your function here!
def modify_dict(a_dictionary):
    # print(a_dictionary)
    return_dictionary ={}
    for (key, values) in a_dictionary.items():
        # print(key)
        # print(values)
        if key[0].isupper():
            return_dictionary[key] = values
        else:
            pass
    return return_dictionary




#Below are some lines of code that will test your function.
#You can change the value of the variable(s) to test your
#function with different inputs.
#
#If your function works correctly, this will originally
#print (although the order of the keys may vary):
#  {'Diaddigo':'Joshua', 'Elliott':'jackie'}


my_dict = {'Joshua':'Diaddigo', 'joyner':'David', 'Elliott':'jackie', 'murrell':'marguerite'}
print(modify_dict(my_dict))


#sample answer

def modify_dict(name_dict):

    #The hint in the original instructions tells you that
    #we can't iterate through the dictionary and delete
    #items from it at the same time. Why not? When
    #iterating, Python keeps a pointer to the current item.
    #When you delete an item, every item slides back one
    #spot -- so the pointer is now pointing to what *was*
    #the next item. Then, when it gets the next item, it
    #skips what was actually the next item.
    #
    #So instead, we want to first make a list of all the
    #keys we want to delete. First, we initialize an
    #empty list:

    del_list = []

    #Then we iterate through the keys:

    for key in name_dict:

        #And if the key is not capitalized (e.g. if it
        #does not equal the capitalized version of
        #itself)...

        if key != key.capitalize():

            #...then we add it to our list of keys to
            #delete:

            del_list.append(key)

    #Once that's done, del_list has a list of all the
    #keys in name_dict to delete. Now we want to iterate
    #through the keys we stored into del_list. Note that
    #this is okay because we're iterating through del_list
    #and deleting from name_dict, *not* iterating through
    #name_dict:

    for key in del_list:
        del name_dict[key]

    #After that, name_dict is modified with the new value,
    #so we just return it:

    return name_dict



my_dict = {'Joshua':'Diaddigo', 'joyner':'David', 'Elliott':'jackie', 'murrell':'marguerite'}
print(modify_dict(my_dict))











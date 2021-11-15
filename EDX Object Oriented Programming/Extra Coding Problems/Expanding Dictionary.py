#Write a function called add_to_dictionary. add_to_dictionary
#should have three parameters: a dictionary, a potential new
#key, and a potential new value.
#
#add_to_dictionary should add the given key and value to the
#dictionary if the key is of a legal type to be used as a
#dictionary key.
#
#If the key is a legal type to be used as a dictionary key,
#return the resultant dictionary.
#
#If the key is _not_ a legal type to be used as a dictionary
#key, return the string "Error!"
#
#Remember, only immutable types can be used as dictionary
#keys. If you don't remember which types are immutable or
#how to check a value's type, don't fret: there's a way
#to do this without checking them directly!


#Write your function here!
def add_to_dictionary(a_dict, a_value, a_key):
    try:
        a_dict[a_value]= a_key
        return a_dict
    except TypeError:
        return "Error!"




#Below are some lines of code that will test your function.
#You can change the value of the variable(s) to test your
#function with different inputs.
#
#If your function works correctly, this will originally
#print:
#{1: "a", 2: "b", 3: "c", 4: "d"}
#Error!
a_dictionary = {1: "a", 2: "b", 3: "c"}
print(add_to_dictionary(a_dictionary, 4, "d"))
print(add_to_dictionary(a_dictionary, [4, 5, 6], "e"))

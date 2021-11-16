#Write a function called concrete_names. concrete_names takes
#as input one parameter, a dictionary. Each key in the
#dictionary will be a string corresponding to a first name.
#Each value in the dictionary will be a list of last names.
#
#concrete_names should return a list of lists. Each list
#should be an alphabetically-sorted list of names constructed
#by putting each first name together with each of its last
#names. The lists themselves should also be in alphabetical
#order by what first name is shared by all names in the list.
#
#For example, this could be one of the dictionaries your
#function receives:
#
# {"David": ["Beckham", "Tennant", "Joyner"],
#  "Ananya": ["Agarwal", "Chatterjee", "Birla", "Roy"],
#  "Ines": ["Sainz", "Melchor", "Suarez"]}
#
#Your function would then return:
#
# [["Ananya Agarwal", "Ananya Birla", "Ananya Chatterjee", "Ananya Roy"],
#  ["David Beckham", "David Joyner", "David Tennant"],
#  ["Ines Melchor", "Ines Sainz", "Ines Suarez"]]
#
#HINT: To get a list of the keys of a dictionary in alphabetical
#order, use this code:
#
# the_keys = list(a_dict.keys())
# the_keys.sort()


#Write your function here!
def concrete_names(a_dict):
    ret_list = []


    the_keys = list(a_dict.keys())
    the_keys.sort()
    for i in range(0, len(the_keys)):
        sname_list = (a_dict[the_keys[i]])
        sname_list.sort()
        ret1= []
        # ret2= []
        for each_sname in sname_list:
            ret1 = [the_keys[i], each_sname ]

            ret_list.append(ret1)
    return ret_list
#Below are some lines of code that will test your function.
#You can change the value of the variable(s) to test your
#function with different inputs.
#
#If your function works correctly, this will originally
#print:
#
#[["Ananya Agarwal", "Ananya Birla", "Ananya Chatterjee", "Ananya Roy"], ["David Beckham", "David Joyner", "David Tennant"], ["Inés Melchor", "Inés Sainz", "Inés Suarez"]]
print(concrete_names({"David": ["Beckham", "Tennant", "Joyner"], "Ananya": ["Agarwal", "Chatterjee", "Birla", "Roy"], "Ines": ["Sainz", "Melchor", "Suarez"]}))



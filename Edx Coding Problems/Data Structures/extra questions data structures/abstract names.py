#Write a function called abstract_names. abstract_names
#should have one parameter: a list of lists. Each list will
#be a list of strings, each with a first name and a last
#name, and each with the same first name.
#
#For example, this could be one list of lists your function
#might receive:
#
# [["David Joyner", "David Tennant", "David Beckham"],
#  ["Ananya Birla", "Ananya Agarwal", "Ananya Chatterjee", "Ananya Roy"],
#  ["Inés Sainz", "Inés Suarez", "Inés Melchor"]]
#
#abstract_names should return a dictionary. The keys to the
#dictionary should be the first names, and the values should
#be lists of the associated last names. The last names should
#be sorted alphabetically.
#
#For example, with the list above, the dictionary returned by
#abstract_names would be:
#
# {"David": ["Beckham", "Joyner", "Tennant"],
#  "Ananya": ["Agarwal", "Birla", "Chatterjee", "Roy"],
#  "Inés": ["Melchor", "Sainz", "Suarez"]}


#Write your function here!
def abstract_names(a_list_of_list):
    output_dictionary ={}
    for each_item in a_list_of_list:
        # print(each_item)
        sname_list =[]
        for each_name in each_item:
            # print(each_name)
            dict_key = each_name.split()[0]
            dict_surname = each_name.split()[1]
            sname_list.append(dict_surname)
        # print(sname_list)
        sname_list.sort()
        # print(dict_key)
        output_dictionary[dict_key] = sname_list
    return output_dictionary


#Below are some lines of code that will test your function.
#You can change the value of the variable(s) to test your
#function with different inputs.
#
#If your function works correctly, this will originally
#print (although the order of the keys may vary):
#
#{"David": ["Beckham", "Joyner", "Tennant"], "Ananya": ["Agarwal", "Birla", "Chatterjee", "Roy"], "Inés": ["Melchor", "Sainz", "Suarez"]}
names = [["David Joyner", "David Tennant", "David Beckham"], ["Ananya Birla", "Ananya Agarwal", "Ananya Chatterjee", "Ananya Roy"], ["Ines Sainz", "Ines Suarez", "Ines Melchor"]]
print(abstract_names(names))



#Write a function called pivot_library. pivot_library takes
#as input one parameter, a list of 3-tuples. Each tuple in
#the list has three items: the first item is a movie title
#(a string), the second item is the movie's release year (an
#integer), and the third item is the movie's total gross (an
#integer).
#
#pivot_library should return a dictionary. In the dictionary
#that it returns, the keys should be the movie names, and the
#values should be 2-item tuples. In each tuple, the first
#item should be the release year, and the second item should
#be the total gross.
#
#Hint: Unpack the tuple to variables first, then create the
#new dictionary item.
#
#For example:
#
# movies = [("Avatar", 2009, 760507625),
#           ("Black Panther", 2018, 699931862)]
# pivot_library(movies)
#   -> {"Avatar": (2009, 760507625),
#       "Black Panther": (2018, 699931862)}


#Write your function here!
def pivot_library(a_list):
    r_dictionary = {}
    for each_tuple in a_list:
        dict_value = []
        # print(each_tuple)
        dict_value.append(each_tuple[1])
        dict_value.append(each_tuple[2])
        r_dictionary[each_tuple[0]]=tuple(dict_value)
    print(r_dictionary)
    return r_dictionary



#Below are some lines of code that will test your function.
#You can change the value of the variable(s) to test your
#function with different inputs.
#
#If your function works correctly, this will originally
#print (although the order of the keys may vary):
#
#{"Avatar": (2009, 760507625), "Black Panther": (2018, 699931862)}
movies = [("Avatar", 2009, 760507625), ("Black Panther", 2018, 699931862)]
print(pivot_library(movies))



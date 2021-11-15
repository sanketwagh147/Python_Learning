#Write a function, called lucky_sevens, that takes in one
#parameter, a list of integers, and returns True if the list
#has three '7's  in a row and False if the list doesn't.
#
#For example:
#
#  lucky_sevens([4, 7, 8, 2, 7, 7, 7, 3, 4]) -> True
#  lucky_sevens([4, 7, 7, 2, 8, 3, 7, 4, 3]) -> False
#
#Hint: As soon as you find one instance of three sevens, you
#could go ahead and return True -- you only have to find it
#once for it to be True! Then, if you get to the end of the
#function and haven't returned True yet, then you might
#want to return False.


#Write your function here!
def lucky_sevens(a_list_of_integer):
    a_string_of_list="".join([str(element) for element in a_list_of_integer])
    # print(a_string_of_list)
    if "777" in a_string_of_list:
        return True
    else:
        return False



#Below are some lines of code that will test your function.
#You can change the value of the variable(s) to test your
#function with different inputs.
#
#If your function works correctly, this will originally
#print: True, then False
print(lucky_sevens([4, 7, 8, 2, 7, 7, 7, 3, 4]))
print(lucky_sevens([4, 7, 7, 2, 8, 3, 7, 4, 3]))


# Edx Solution

#When you were first thinking about this problem, you might have
#thought, "Well if I merge them all into a string, I can just
#do return "777" in a_list_as_string". You might have also
#thought, "I can do ''.join(a_list) to convert it to a string!"
#
#If you tried that, clever! However, you found that it wouldn't
#work. join() only works on lists of strings. You could have
#then run a loop on each item in a_list, converting it to a
#string, and then returning "777" in a_list, as shown below:
#
#def lucky_sevens(a_list):
#
#    for i in range(len(a_list)):
#        a_list[i] = str(a_list[i]))
#    return "777" in a_list
#
#However, the problem here is that you're modifying the list.
#Remember, lists are mutable, so this actually changes the values
#of the list. We probably didn't want to do that. Instead, we
#can make use of a handy Python function called map():

def lucky_sevens(a_list):

    #map() takes two arguments: a function and a list. It returns
    #a new list created by applying that function to each item in
    #that list:

    a_list_as_strings = map(str, a_list)

    #So, this effectively duplicates the code in the comment above,
    #but without changing a_list. It applies the function str() to
    #each item in a_list, and returns a list of the results.
    #
    #Then, we can check if "777" is in the result of joining that
    #list of strings:

    a_list_as_one_string = "".join(a_list_as_strings)
    return "777" in a_list_as_one_string

    #All of which could becompressed down to one line:
    #return "777" in "".join(map(str, a_list))


#Don't worry if this is confusing -- the map() function is a little
#out of scope for our material. Note, though, that if you had Googled
#"Python join list of ints", you'll find an answer that explains how
#to use the function. If you need to do something you don't know how
#to do, search for a solution!


print(lucky_sevens([4, 7, 8, 2, 7, 7, 7, 3, 4]))
print(lucky_sevens([4, 7, 7, 2, 8, 3, 7, 4, 3]))





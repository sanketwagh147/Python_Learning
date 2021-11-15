#Write a function called duplicate_from_list. duplicate_from_list
#should have two parameters: a list of strings and a list of
#integers.
#
#The list of integers represents the indices of the items to
#duplicate from the list of strings. A duplicated item should
#be added to the beginning of the list, in the order given by
#the indices.
#
#For example:
#
# duplicate_from_list(["a", "b", "c", "d"], [0, 3, 1])
#
#...would return the list ["a", "d", "b", "a", "b", "c", "d"].
#"a" is at index 0, "d" is at 3, and "b" is at 1; so, each are
#duplicated and added to the start of the list in that order. If
#an index appears twice in the list, its corresponding value
#should be duplicated twice.
#
#Note, though, that the indices in the second list refer to
#where the character was found _originally_. Once "a" is
#duplicated and added at the start, the indices of the other
#characters shift; but the index 3 still refers to the string
#that was originally at index 3 ("d").
#
#HINT: There are several ways to do this. If you get stuck on
#one, try to think if there is a very different approach!


#Write your function here!
def duplicate_from_list(string_list, int_list):
    extend_list = []
    for each in int_list:
        extend_list.append(string_list[each])
    extend_list.extend(string_list)
    return extend_list


#Below are some lines of code that will test your function.
#You can change the value of the variable(s) to test your
#function with different inputs.
#
#If your function works correctly, this will originally
#print:
#['a', 'd', 'b', 'a', 'b', 'c', 'd']
#['b', 'a', 'b', 'a', 'b', 'c', 'd']
#['a', 'b', 'c', 'd', 'a', 'b', 'c', 'd']
print(duplicate_from_list(["a", "b", "c", "d"], [0, 3, 1]))
print(duplicate_from_list(["a", "b", "c", "d"], [1, 0, 1]))
print(duplicate_from_list(["a", "b", "c", "d"], [0, 1, 2, 3]))




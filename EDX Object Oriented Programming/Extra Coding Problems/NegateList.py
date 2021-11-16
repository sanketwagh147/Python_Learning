#Write a function called negate_list. negate_list should havetwo
#parameters: a list of floats and a list of integers.
#
#The list of integers will represent indices for the list of
#floats. negate_list should switch the sign of all the floats
#located at those indices.
#
#For example:
#
# float_list = [1.0, -2.0, -3.0, 4.0]
# index_list = [0, 2]
# negate_list(float_list, index_list) -> [-1.0, -2.0, 3.0, 4.0]
#
#After calling negate_list, the floats at indices 0 and 2 have
#switched signs (1.0 to -1.0 and -3.0 to 3.0).
#
#Note that it may be the case that the same index is present
#in the second twice. If this happens, you should switch the
#boolean at that index twice. For example:
#
# float_list = [1.0, -2.0, -3.0, 4.0]
# index_list = [0, 2, 2]
# negate_list(float_list, index_list) -> [-1.0, -2.0, -3.0, 4.0]
#
#2 is in index_list twice, so the float at index 2 is
#switched twice: negative to positive, then positive back
#to negative.
#
#Hint: Remember you can change a list in place! You don't
#need to create a new list.


#Write your function here!
def negate_list(float_list, int_list):
    for each in int_list:
        float_list[each] = -(float_list[each])
    return float_list


#Below are some lines of code that will test your function.
#You can change the value of the variable(s) to test your
#function with different inputs.
#
#If your function works correctly, this will originally
#print:
#[-1.0, -2.0, 3.0, 4.0]
#[-1.0, -2.0, -3.0, 4.0]
print(negate_list([1.0, -2.0, -3.0, 4.0], [0, 2]))
print(negate_list([1.0, -2.0, -3.0, 4.0], [0, 2, 2]))




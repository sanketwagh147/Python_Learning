#Write a function called digit_count. digit_count should
#take as input a number, which could be either a float or an
#integer. It should return a dictionary whose keys are digits,
#and whose values are the number of times that digit appears
#in the number.
#
#The dictionary should NOT contain any numerals that do not
#occur at all in the number, and it should also not contain
#the decimal point character if the number is a decimal.
#
#For example:
#
#  digit_count(11223) -> {1: 2, 2: 2, 3: 1}
#  digit_count(3.14159) -> {3: 1, 1: 2, 4: 1, 5: 1, 9: 1}
#
#Hint: You should probably convert the number to a string to
#count the digits, but convert the individual digits back to
#integers to use as keys to the dictionary.

#Write your function here!
def digit_count(a_number):
    output_dictionary = {}
    count = 0
    a_number_as_str = str(a_number)
    # print(a_number_as_str)
    a_number_as_str = a_number_as_str.replace(".", "")
    for each in a_number_as_str:
        # print(each)
        each = int(each)
        if each not in output_dictionary.keys():
            output_dictionary[each] = 1
        else:
            output_dictionary[each] = output_dictionary[each] + 1
    return output_dictionary


#Below are some lines of code that will test your function.
#You can change the value of the variable(s) to test your
#function with different inputs.
#
#If your function works correctly, this will originally
#print (although the order of the keys may vary):
#
#{1: 2, 2: 2, 3: 1}
#{3: 1, 1: 2, 4: 1, 5: 1, 9: 1}
print(digit_count(11223))
print(digit_count(3.14159))



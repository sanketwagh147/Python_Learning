a_string = "F12dav^f%$25d"

#You may modify the lines of code above, but don't move them!
#When you Submit your code, we'll change these lines to
#assign different values to the variables.

#a_string is a string of random characters. Write some code
#that adds all the digits that appear in the string and prints
#their sum.
#
#For example, the digits in the string above are 1, 2, 2, and 5,
#so your code would print 10.
#
#Remember, you can iterate over each character in a string with
#this syntax:
#
#for a_character in a_string:
#
#Remember also, you can check if a character is in a list of other
#characters within this syntax:
#
#if a_character in "ABCDEFG":
#
#If there are no digits in the string, print 0.


#Add your code here!
the_sum = 0
for char in a_string:
    # print(char)
    if char in [str(x) for x in (range(0, 10))]:
        # print(char)
        the_sum += int(char)
print(the_sum)


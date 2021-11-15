#A palindrome is a sequence of letters that is the same
#forward and backward. For example, "racecar" is a
#palindrome.
#
#Write a function called create_palindrome. The function should
#have one parameter, a string. The function should return the
#string as a palindrome.
#
#If the string was not already a palindrome, the function should
#return a new string made from the original string and the
#reverse of the original string. For example:
#
# create_palindrome("abc") -> "abccba"
#
#However, if the string _is_ already a palindrome, the function
#should just return the original string by itself. For example:
#
# create_palindrome("racecar") -> "racecar"
#
#In determining whether a string is a palindrome or not, you
#should ignore punctuation, capitalization and spaces. For
#example:
#
# create_palindrome("Madam in Eden, I'm Adam") -> "Madam in Eden, I'm Adam"
#
#In creating a palindrome, though, you should use the original
#formatting:
#
# create_palindrome("Hello there!") -> "Hello there!!ereht olleH"
#
#You may assume that the only characters in the string will
#be letters, spaces, apostrophes, commas, periods, and
#question marks.
#
#Hint: Before checking if the string is a palindrome, get
#rid of the spaces and punctuation marks using the replace()
#method and convert the entire string to upper or lower
#case using the upper() or lower() methods. Remember, though,
#to keep the original string as your result should preserve
#the original punctuation and capitalization.
#
#Hint 2: There are multiple ways to do this! If you're stuck
#on one way, try a different one. You could use string
#slicing, a for loop, or some string methods. Or, try
#printing the string at different stages to see what's going
#wrong!
def is_palindrome(a_string):
    string_lower = a_string.lower()
    empty_string =""
    for char in string_lower:
        if char.isalpha():
            empty_string += char
    # print(empty_string)
    if empty_string == empty_string[::-1]:
        return True
    else:
        return False

#Write your function here!
def create_palindrome(a_str):
    if is_palindrome(a_str):
        return a_str
    else:
        return a_str+a_str[::-1]

#Below are some lines of code that will test your function.
#You can change the value of the variable(s) to test your
#function with different inputs.
#
#If your function works correctly, this will originally
#print:
#racecar
#Madam in Eden, I'm Adam
#Mister in Eden, I'm EveevE m'I ,nedE ni retsiM
print(create_palindrome("racecar"))
print(create_palindrome("Madam in Eden, I'm Adam"))
print(create_palindrome("Mister in Eden, I'm Eve"))




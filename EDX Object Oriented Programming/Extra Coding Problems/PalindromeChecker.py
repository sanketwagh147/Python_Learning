#Write a function called is_palindrome. The function should
#have one parameter, a string. The function should return
#True if the string is a palindrome, False if not.
#
#A palindrome is a sequence of letters that is the same
#forward and backward. For example, "racecar" is a
#palindrome. In determining whether a string is a palindrome
#or not, you should ignore punctuation, capitalization and
#spaces. For example, "Madam in Eden, I'm Adam" is a
#palindrome.
#
#You may assume that the only characters in the string will
#be letters, spaces, apostrophes, commas, periods, and
#question marks.
#
#Hint: Before checking if the string is a palindrome, get
#rid of the spaces and punctuation marks using the replace()
#method and convert the entire string to upper or lower
#case using the upper() or lower() methods.
#
#Hint 2: There are multiple ways to do this! If you're stuck
#on one way, try a different one. You could use string
#slicing, a for loop, or some string methods. Or, try
#printing the string at different stages to see what's going
#wrong!

#Write your function here!  
# def is_palindrome(a_string): 
#     string_lower = a_string.lower()
#     empty_string ="" 
#     for char in string_lower:
#         if char.isalpha():
#             empty_string += char
#     # print(empty_string)
#     if empty_string == empty_string[::-1]:
#         return True
#     else:
#         return False
#Below are some lines of code that will test your function.
#You can change the value of the variable(s) to test your
#function with different inputs.
#
#If your function works correctly, this will originally
#print: True, True, False, each on their own line.

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
print(is_palindrome("Never Odd or Even"))
print(is_palindrome("abc"))
print(is_palindrome("kayak"))




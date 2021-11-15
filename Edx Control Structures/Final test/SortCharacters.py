#Write a function called sort_characters. sort_characters
#should take as input one parameter, a string.
#
#sort_characters should return a string such that all the
#characters in the original string are still present, but
#in a different order. All the capital letters should appear
#first, then all the lower-case letters, then all the
#numerals, then all the punctuation marks. Within each
#category, the letters should appear in the same order as
#in the original string.
#
#For example, for the string "DavidJoyner", the function
#would return "DJavidoyner": the capital letters (DJ) first,
#then the lower case, all in the same order in which they
#originally appeared.
#
#Some more examples:
#
# sort_characters("GeorgiaTech") -> "GTeorgiaech"
# sort_characters("ThisIsCS1301!") -> "TICShiss1301!"
# sort_characters("One1.Two2?Three3!") -> "OTTnewohree123.?!"
# sort_characters("CS1301") -> "CS1301"
#
#You may use the ord() function to get a letter's ordinal
#number. The ordinal numbers you might need to use are:
#
# - Capital letters: 65 ("A") through 90 ("Z").
# - Lower-case letters: 97 ("a") through 122 ("z").
# - Numerals: 48 ("0") through 57 ("9").
# - Punctuation: Any other ordinals (for this problem).
#
#Hint: You don't have to use ordinal numbers; you can use the
#in operator instead, e.g. "a" in "abcde".
#
#Hint 2: If you're stuck, think of this problem in two stages:
#dividing the characters into their categories, and then
#recombining them into their results!


#Write your function here!
def sort_characters(a_string):
    ret_string = ""
    for char in a_string:
        if char.isupper():
            ret_string += char
    for char in a_string:
        if char.islower():
            ret_string += char
    for char in a_string:
        if char.isdigit():
            ret_string += char
    for char in a_string:
        if char.isalnum() == False:
            ret_string += char
    return ret_string


#Below are some lines of code that will test your function.
#You can change the value of the variable(s) to test your
#function with different inputs.
#
#If your function works correctly, this will originally
#print:
#DJavidoyner
#GTeorgiaech
#TICShiss1301
#OTTnewohree123.?!
#CS1301
print(sort_characters("DavidJoyner"))
print(sort_characters("GeorgiaTech"))
print(sort_characters("ThisIsCS1301!"))
print(sort_characters("One1.Two2?Three3!"))
print(sort_characters("CS1301"))







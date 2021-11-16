#Write a function called are_anagrams. The function should
#have two parameters, a pair of strings. The function should
#return True if the strings are anagrams of one another,
#False if they are not.
#
#Two strings are considered anagrams if they have only the
#same letters, as well as the same count of each letter. For
#this problem, you should ignore spaces and capitalization.
#
#So, for us: "Elvis" and "Lives" would be considered
#anagrams. So would "Eleven plus two" and "Twelve plus one".
#
#Note that if one string can be made only out of the letters
#of another, but with duplicates, we do NOT consider them
#anagrams. For example, "Elvis" and "Live Viles" would not
#be anagrams.


#Write your function here!
def are_anagrams(str_1, str_2):
    str_1 =str_1.lower().replace(" ", "")
    str_2 = str_2.lower().replace(" ", "")
    list1 = [i for i in str_1]
    # str_1_1 = str_1.swapcase()
    # list2 = [i for i in str_1_1]
    # list1.append(" ")
    # list1.extend(list2)
    print(list1)
    condition = bool
    print(len(str_1), len(str_2))
    if len(str_1) == len(str_2):
        for char in str_2:
            print(char)
            if char in list1:
                condition = True
            else:
                return False
        return condition
    return False



#Below are some lines of code that will test your function.
#You can change the value of the variable(s) to test your
#function with different inputs.
#
#If your function works correctly, this will originally
#print: True, False, True, False, each on their own line.
# print(are_anagrams("Elvis", "Lives"))
# print(are_anagrams("Astronomer", "Moon Starer"))
print(are_anagrams("Christmas", "Shirt Cash"))
# print(are_anagrams("Elvis", "Live Viles"))
# print(are_anagrams("Eleven plus two", "Twelve plus one"))
# print(are_anagrams("Nine minus seven", "Five minus three"))
# print(are_anagrams("The Morse Code", "Here Came Pots"))


# EDX sampkle

# def are_anagrams(first_word, second_word):
#     first_word = first_word.lower()
#     second_word = second_word.lower()
#     first_word = first_word.replace(' ', '')
#     second_word = second_word.replace(' ', '')
#
# #For me, the first thought was to store the letters of the first word
# #into a list and then iterate through the second word and remove the letter stored
# #if it existed in the list.
#
# #SO, I create an empty list called 'letters'
#
#     letters = []
#
# #I then iterate through my first word and the append all the characters
#
#     for char in first_word:
#         letters.append(char)
#
# #I then iterate through my second word and see if the letter I am currently
# #iterating through is in my list.
# #If it is in my list, then I remove that character (this avoids duplicates)
# #and if my current letter is not in my list then I automatically return False
# #since that means my second word has a letter that my first word doesn't!
#
#     for char in second_word:
#         if char not in letters:
#             return False
#         letters.remove(char)
#
# #At the very end when we are done iterating through, I return the boolean value
# #of whether my length of list is equal to 0. I do not simply return True because
# #there may be cases where my first word will have letters that my second letter
# #might not have. ie. first = hello, second = helo (list would still contain 'l')
#
#     return len(letters) == 0

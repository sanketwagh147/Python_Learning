#Pig Latin is a fictitious language. To translate a word into
#Pig Latin, you would take the consonants up until the first
#vowel, move them to the end, and add "ay" to the end.
#
#For example:
#
# pig -> igpay
# david -> avidday
# trash -> ashtray
# scram -> amscray
# translate -> anslatetray
#
#Write a function called to_pig_latin. to_pig_latin will take
#as input a single word, and return the Pig Latin version of
#the word.
#
#For the purposes of this problem, only a, e, i, o, and u are
#vowels: y is a consonant. You may assume that the word will
#start with at least one consonant, that the letters to move to
#the end will always be the consonants until the first vowel,
#and that the string will be all lower-case.


#Write your function here!
def to_pig_latin(a_str):
    ret_char = ""
    vowel_list = ["a", "e", "i", "o", "u"]
    for i in range(0, len(a_str)):
        if a_str[i] in vowel_list:
            ret_char += a_str[i:]
            # print(ret_char)
            ret_char += a_str[:i]
            # print(ret_char)
            ret_char += "ay"
            # print(ret_char)
            return ret_char





#Below are some lines of code that will test your function.
#You can change the value of the variable(s) to test your
#function with different inputs.
#
#If your function works correctly, this will originally
#print the same results as in the examples above.
# print(to_pig_latin("pig"))
# print(to_pig_latin("david"))
print(to_pig_latin("trash"))
print(to_pig_latin("scram"))
print(to_pig_latin("translate"))




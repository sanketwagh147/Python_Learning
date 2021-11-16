#Do not change the line of code below. It's at the top of
#the file to ensure that it runs before any of your code.
#You will be able to access french_dict from inside your
#function.
french_dict = {"me": "moi", "hello": "bonjour",
               "goodbye": "au revoir", "cat": "chat",
               "dog": "chien", "and": "et"}

#Write a function called french2eng that takes in one string
#parameter called sentence. french2eng should look at each
#word in the sentence and translate it into French if it is
#found in the dictionary, french_dict. If a word is not found
#in the dictionary, do not translate it: use the original
#word. Then, the function should return a string of the
#translated sentence.
#
#You may assume that the sentence you're translating has no
#punctuation. However, you should convert it to lower case
#before translating.
#
#For example:
def french2eng(a_string):
    # print(a_string)
    returning_string=""
    a_string_to_list = a_string.lower().split()
    # print(a_string_to_list)
    for i in range(0, len(a_string_to_list)):
        # print(a_string_to_list[i])
        if a_string_to_list[i] in french_dict:
            add_word = french_dict[a_string_to_list[i]]
            # print(add_word)
            # print(a_string_to_list[i]+" is in french dicitionary")
            returning_string += add_word+" "

        else:
            add_word = a_string_to_list[i]
            # print(add_word)
            returning_string += add_word+" "
    return returning_string

#  french2eng("Hello it's me") -> "bonjour it's moi"
#
#Hint: Use .split() to get a list of strings representing
#each word in the string, then use ' '.join to merge the
#translated list back into one string.
#
#Hint 2: Remember, lists are mutable, so we can change
#individual items in the list. However, to change an item
#in a list, we must change it using its index. We can
#write lines like my_words[1] = new_word.
#
#Hint 3: If you're stuck, try breaking it down into small
#parts. How do you access an item from a list? How do you
#look up a key in a dictionary? How do you change the
#value of an item in a list? How do you check if a key is
#in the dictionary?


#Write your function here!



#Below are some lines of code that will test your function.
#You can change the value of the variable(s) to test your
#function with different inputs.
#
#If your function works correctly, this will originally
#print: bonjour it's moi
print(french2eng("Hello it's me"))


#sample answer

sentence = sentence.lower()
sentsplit = sentence.split(" ")
for i in range(len(sentsplit)):
    if sentsplit[i] in french_dict:
        sentsplit[i] = french_dict[sentsplit[i]]
return " ".join(sentsplit)


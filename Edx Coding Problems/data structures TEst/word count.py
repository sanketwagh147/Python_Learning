#Write a function called word_count. word_count should take
#as input a list. You may assume every item in the list will
#be a string.
#
#word_count should return a dictionary, where the keys are the
#words and the values are the number of times each word appeared
#in the list. The keys should all be lower-case, and you should
#ignore case when counting words (for instance, "cat", "CAT",
#and "Cat" would all count towards the key "cat").
#
#For example:
#
#  word_count(["cat", "CAT", "dog", "DOG"]) -> {"cat": 2, "dog": 2}
#  word_count(["Georgian", "Tech", "Georgia", "Tech"]) ->
#             {"Georgian": 1, "Tech": 2, "Georgia": 1}


#Write your function here!
def word_count(a_list):
    lower_list = []
    ret_dict = {}
    for each_item in a_list:
        lower = each_item.lower()
        lower_list.append(lower)
    # print(lower_list)
    # no_dup_lower_list = set(lower_list)
    # print(no_dup_lower_list)
    for each_item in lower_list:
        if each_item in ret_dict.keys():
            ret_dict[each_item]+= 1
        else:
            ret_dict[each_item]= 1
    return ret_dict

#Below are some lines of code that will test your function.
#You can change the value of the variable(s) to test your
#function with different inputs.
#
#If your function works correctly, this will originally
#print (although the order of the keys may vary):
#
#{"cat": 2, "dog": 2}
#{"Georgian": 1, "Tech": 2, "Georgia": 1}
print(word_count(["cat", "CAT", "dog", "DOG"]))
print(word_count(["Georgian", "Tech", "Georgia", "Tech"]))



#Write a function called rabbit_hole. rabbit_hole should have
#two parameters: a dictionary and a string. The string may be
#a key to the dictionary. The value associated with that key,
#in turn, may be another key to the dictionary.
#
#Keep looking up the keys until you reach a key that has no
#associated value. Then, return that key.
#
#For example, imagine if you had the following dictionary.
#This one is sorted to make this example easier to follow:
#
# d = {"bat": "pig", "pig": "cat", "cat": "dog", "dog": "ant",
#      "cow": "bee", "bee": "elk", "elk": "fly", "ewe": "cod",
#      "cod": "hen", "hog": "fox", "fox": "jay", "jay": "doe",
#      "rat": "ram", "ram": "rat"}
#
#If we called rabbit_hole(d, "bat"), then our code should...
#
# - Look up "bat", and find "pig"
# - Look up "pig", and find "cat"
# - Look up "cat", and find "dog"
# - Look up "dog", and find "ant"
# - Look up "ant", and find no associated value, and so it would
#   return "ant".
#
#Other possible results are:
#
# rabbit_hole(d, "bat") -> "fly"
# rabbit_hole(d, "ewe") -> "hen"
# rabbit_hole(d, "jay") -> "doe"
# rabbit_hole(d, "yak") -> "yak"
#
#Notice that if the initial string passed in is not a key in
#the dictionary, that string should be returned as the result as
#well.
#
#Note, however, that it is possible to get into a loop. In the
#dictionary above, rabbit_hole(d, "rat") would infinitely go
#around between "rat" and "ram". You should prevent this: if a
#key is ever accessed more than once (meaning a loop has been
#reached), return the boolean False.
#
#Hint: If you try to access a value from a dictionary that does
#not exist, a KeyError will be raised.



#Write your function here!
def rabbit_hole(a_dict, a_str):
     try:
          if a_dict[a_str] not in a_dict.keys():
               # print("1")
               # print("1.1")
               ret = a_dict[a_str]
               # print("1.2")
               return ret

          else:
               # print("2")
               # print(a_dict[a_dict[a_str]])
               try:
                    return rabbit_hole(a_dict, a_dict[a_str])
               except RecursionError:
                    return False
     except KeyError :
          return a_str

#Below are some lines of code that will test your function.
#You can change the value of the variable(s) to test your
#function with different inputs.
#
#If your function works correctly, this will originally
#print: ant, hen, doe, yak, False, each on their own line.
d = {"bat": "pig", "pig": "cat", "cat": "dog", "dog": "ant",
     "cow": "bee", "bee": "elk", "elk": "fly", "ewe": "cod",
     "cod": "hen", "hog": "fox", "fox": "jay", "jay": "doe",
     "rat": "ram", "ram": "rat"}

print(rabbit_hole(d, "bat"))
print(rabbit_hole(d, "ewe"))
print(rabbit_hole(d, "jay"))
print(rabbit_hole(d, "yak"))
print(rabbit_hole(d, "rat"))



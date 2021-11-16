#Imagine you're writing a program to help an evil genius name
#his nefarious creations. To start the naming process, he
#gives you a word or phrase. To generate the name, you replace
#the spaces in the phrase (if there are any) with hyphens,
#and then add the suffix 'inator' to the end. But a name like
#'Translateinator' would look silly having an 'e' right next
#to the 'i', so before you add 'inator', you want to remove
#any vowels occuring at the very end of the phrase.
#
#Write a function called get_inator. get_inator should have
#one parameter, a string. It should find the name of the
#inator and return it.
#
#For example:
#
# get_inator("Destruct") -> "Destructinator"
# get_inator("Deflate") -> "Deflatinator" (notice the 'e' in 'Deflate' was removed!)
# get_inator("Age Accelerator") -> "Age-Acceleratorinator"
# get_inator("Copy and Paste") -> "Copy-and-Pastinator"
#
#For the purposes of this problem, only a, e, i, o, and u are
#vowels: y is a consonant. The only changes you make should
#be (1) replacing spaces with hyphens, (2) removing the vowel
#at the end if there is one, and (3) adding 'inator' to the
#end.


#Write your function here!
def get_inator(a_string):
    a_string = a_string.replace(" ", "-")
    # print(a_string)
    if a_string[-1] in ["a", "e", "i","o", "u"]:
        a_string =a_string[:-1]
        return a_string + "inator"
    else:
        return a_string + "inator"

#Below are some lines of code that will test your function.
#You can change the value of the variable(s) to test your
#function with different inputs.
#
#If your function works correctly, this will originally
#print the same results as in the examples above.
print(get_inator("Destruct"))
print(get_inator("Deflate"))
print(get_inator("Age Accelerator"))
print(get_inator("Copy and Paste"))



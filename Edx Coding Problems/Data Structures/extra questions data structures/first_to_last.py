#Write a function called first_to_last. first_to_last should
#take as input a string representing a filename. Inside the
#file will be some text on each line; some lines will contain
#integers, while others will contain strings of other
#characters.
#
#first_to_last should return a tuple containing the first and
#last strings in the file alphabetically. It should ignore any
#lines that contain integers.
#
#For example, in the dropdown in the top left you'll find a
#file named FirstLastInput.txt. Ignoring numerals, the first
#string alphabetically is appsp, and the last string
#alphabetically is zzffs. So, first_to_last("FirstLastInput.txt")
#would return the tuple ("appsp", "zzffs").
#
#You may assume that every line in the file contains either
#all numerals or all lower-case letters; there will be no lines
#with both numerals and letters, nor any capital letters.
#Write your function here!
def first_to_last(a_file_name):
    a_list = []
    b_list =[]
    a_file = open(a_file_name, "r")
    a_str = a_file.read()
    # print(a_str)
    a_list = a_str.splitlines()
    a_list.sort()
    for each_item in a_list:
        if each_item.isalpha():
            b_list.append(each_item)
    # print(b_list)
    return (b_list[0], b_list[-1])

    # print(a_list)




#Below are some lines of code that will test your function.
#You can change the value of the variable(s) to test your
#function with different inputs.
#
#If your function works correctly, this will originally
#print: ("appsp", "zzffs")
print(first_to_last("FirstLastInput.txt"))



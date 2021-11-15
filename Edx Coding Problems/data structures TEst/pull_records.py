#Write a function called pull_records. first_to_last should
#have two parameters: a string representing a filename, and a
#list of integers. Inside the file, there will be some text on
#each line.
#
#pull_records should return as a list the text on each line of
#the file represented in the list of integers. For example, if
#the list of integers was [0, 4, 8], then pull_records should
#return the text from lines 0, 4, and 8 as a list. The order of
#the lines in the list must match the order of the integers.
#
#In the dropdown in the top left, you can see the contents of
#a file called Some_Records.txt. You'll use this file to test
#your code below. Remember though, we consider the first line
#of the file to be line 0, not line 1.
#
#HINT: Don't forget that if you read the file using methods
#like readlines() or read(), the linebreaks are included. If
#you results seem weirdly split between multiple lines, it
#means you're not removing these line breaks with something
#like the strip() method!


#Write your function here!
def pull_records(a_file_name, list_of_integers):
    data = open(a_file_name)
    ret_list = []
    raw_data = data.read()
    # print(raw_data)
    indexed_list = raw_data.splitlines()
    # print(indexed_list)
    data.close()
    for each in list_of_integers:
        ret_list.append(indexed_list[each])
    return ret_list
#Below are some lines of code that will test your function.
#You can change the value of the variable(s) to test your
#function with different inputs.
#
#If your function works correctly, this will originally
#print: ["need", "delicious", "pies"]
print(pull_records("Some_Records.txt", [0, 4, 8]))



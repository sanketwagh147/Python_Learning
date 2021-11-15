#You've been sent a list of names. Unfortunately, the names
#come in two different formats:
#
#First Middle Last
#Last, First Middle
#
#You want the entire list to be the same. For this problem,
#we'll say you want the entire list to be Last, First Middle.
#
#Write a function called name_refixer. name_refixer should take
#as input the list of strings. You may assume that every string
#will match one of the two formats above: either First Middle Last
#or Last, First Middle.
#
#name_fixer should return a list of names all structured as
#Last, First Middle. If the name was already structured as
#Last, First Middle, it should remain unchanged. If it was
#structured as First Middle Last, then Last should be moved
#to the beginning and a comma should be added after it.
#
#The names should appear in the same order as the original list.
#
#For example:
#
#name_list = ["David Andrew Joyner", "Hart, Melissa Joan", "Cyrus, Billy Ray"]
#name_fixer(name_list) -> ["Joyner, David Andrew", "Hart, Melissa Joan", "Cyrus, Billy Ray"]
#Add your code here!
def name_refixer(a_list_of_string):
    for each_name in a_list_of_string:
        # print(each_name)
        if "," in each_name:
            pass
        else:
            each_name_list=each_name.split()
            # print(each_name_list)
            modified_list=[each_name_list[2],each_name_list[0],each_name_list[1]]
            # print(modified_list)
            name_string=modified_list[0]+","+" "+modified_list[1]+" "+ modified_list[2]
            # print(name_string)
            index_to_be_removed=a_list_of_string.index(each_name)
            # print(index_to_be_removed)
            del a_list_of_string[index_to_be_removed]
            # print(a_list_of_string)
            a_list_of_string.insert(index_to_be_removed, name_string)
            # print(a_list_of_string)
    return a_list_of_string
#Below are some lines of code that will test your function.
#You can change the value of the variable(s) to test your
#function with different inputs.
#
#If your function works correctly, this will originally
#print:
#["Joyner, David Andrew", "Hart, Melissa Joan", "Cyrus, Billy Ray"]
name_list = ["David Andrew Joyner", "Hart, Melissa Joan", "Cyrus, Billy Ray"]
print(name_refixer(name_list))



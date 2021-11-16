#Write a function called string_splitter that replicates the
#function of the string type's split() method, assuming that
#we're splitting at spaces. string_splitter should take as
#input a string, and return as output a list of the
#individual words from the string, assuming that words were
#divided by spaces. The spaces themselves should not be in
#the list that your function returns.
#
#You may assume that there will never be more than one space
#in a row, and that the string will neither start nor end
#with a space. However, you should not assume there will
#always be a space.
#
#You may not use Python's built-in split() method.
#
#For example:
#
#  string_splitter("Hello world") -> ['Hello', 'world']


#Write your function here!
def string_splitter(a_string):
    a_list=[]
    start_index=0
    for each in range(0,len(a_string)):
        # print(a_string[each])
        if a_string[each]==" ":
            # print("find spaces loop successfull")
            # print(each)
            slice_of_sting=a_string[start_index:each]
            # print(slice_of_sting)
            start_index= each+1
            a_list.append(slice_of_sting)
            # print(a_list)
    last_string= a_string[start_index:]
    a_list.append(last_string)
    return a_list
#Below are some lines of code that will test your function.
#You can change the value of the variable(s) to test your
#function with different inputs.
#
#If your function works correctly, this will originally
#print: ['Hello', 'world']
print(string_splitter("Hello world of"))





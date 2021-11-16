#Write a function called all_sum. all_sum should have two
#parameters: a list of integers and a single integer.
#For this description, we'll call the single integer n.
#
#all_sum should modify the list to add the next n all-sum
#numbers to the end of the sequence. An all-sum number is the
#sum of all previous numbers in the sequence.
#
#For example, if the original list given was:
#
# a_list = [1, 2, 3]
#
# Then all_sum(a_list, 3) would return:
#       [1, 2, 3, 6, 12, 24]
#
#All three original numbers in the list are still there, and
#three new ones have been added: the sum of the first three
#numbers (1+2+3 = 6), of the first four (1+2+3+6 = 12), and
#of the first five (1+2+3+6+12 = 24).
#
#You may assume the list parameter will always have at least
#one number.
#
#HINT: Python gets mad if you try to change a list while
#iterating over it with a for-each loop. You'll have to get
#clever with a for or while loop to do this!


#Add your code here!
def all_sum(a_list_of_integers, a_int):
    ret_list = []
    s
    sum = 0
    while a_int > 0:
        a_int -=1
        a_list_of_integers.append(0)
    for each_int in a_list_of_integers:
        sum += each_int

    print(a_list_of_integers)
    return  ret_list




#Below are some lines of code that will test your function.
#You can change the value of the variable(s) to test your
#function with different inputs.
#
#If your function works correctly, this will originally
#print:
#[1, 2, 3, 6, 12, 24]
print(all_sum([1, 2, 3], 3))






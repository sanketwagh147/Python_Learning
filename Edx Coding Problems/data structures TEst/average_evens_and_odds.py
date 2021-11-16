#Write a function called average_evens_and_odds. The function
#should take as input one parameter, a list of integers. The
#function should return a 2-tuple. The first item in the
#2-tuple should be the average of all even numbers in the list;
#the second item in the 2-tuple should be the average of all
#odd numbers in the list. Round your averages to one decimal
#place.
#
#The list may have some strings interspersed in it. These should
#not affect your calculation.
#
#For example, if this was the input list:
#
# [1, 2, 3, 4, "cat", "tech", 5, 6]
#
#Your function would return the tuple: (4.0, 3.0) because 4.0
#is the average of the three even numbers (2, 4, 6) and 3.0 is
#the average of the three odd numbers (1, 3, 5).
#
#HINT: round(the_num, 1) will return the result of rounding
#the_num to one decimal place.


#Add your code here!
def average_evens_and_odds(a_list_of_integers):
    even_count = 0
    sum_even = 0
    sum_odd = 0
    odd_count = 0
    integer_list = [e for e in a_list_of_integers if isinstance(e, int)]
    # print(integer_list)
    for each_int in integer_list:
        if each_int % 2 == 0:
            even_count += 1
            sum_even += each_int
        else:
            odd_count += 1
            sum_odd += each_int
    return (round(sum_even/even_count, 1), round(sum_odd/odd_count, 1))

#Below are some lines of code that will test your function.
#You can change the value of the variable(s) to test your
#function with different inputs.
#
#If your function works correctly, this will originally
#print: (4.0, 3.0)
a_list = [1, 2, 3, 4, "cat", "tech", 5, 6]
(average_evens_and_odds(a_list))






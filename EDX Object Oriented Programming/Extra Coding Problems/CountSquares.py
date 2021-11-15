#Write a function called count_squares. This function
#should take as input a list of integers, and return as
#output a single integer. The number the function returns
#should be the number of perfect squares it found in the
#list of integers. You may assume every number in the list
#is between 1 and 1 billion (1,000,000,000).
#
#For example:
#
# count_squares([1, 2, 3, 4, 5, 6, 7, 8, 9]) -> 3
# count_squares([1, 4, 9, 16, 25, 36, 49, 64]) -> 8
# count_squares([2, 3, 5, 6, 7, 8, 10, 11]) -> 0
#
#For this problem, 0 is considered a square.
#
#Hint: Don't get caught up trying to "remember" how to
#calculate if a number is a square: we've never done it
#before, but we've covered all the tools you need to do it
#in one of several different ways.


#Write your function here!
def count_squares(int_list):
    ret_count = 0
    for each in int_list:
        sqrt = each**0.5
        # print("each:", each)
        # print("sqrt:", sqrt)
        if sqrt.is_integer() == True:
            ret_count += 1
            # print("ret_count:", ret_count)
    return ret_count


#The lines below will test your code. Feel free to modify
#them. If your code is working properly, these will print
#the same output as shown above in the examples.
print(count_squares([1, 2, 3, 4, 5, 6, 7, 8, 9]))
print(count_squares([1, 4, 9, 16, 25, 36, 49, 64]))
print(count_squares([2, 3, 5, 6, 7, 8, 10, 11]))
# a =14.12
# print(a.is_integer())

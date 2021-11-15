#Remember that Fibonacci's sequence is a sequence of numbers
#where every number is the sum of the previous two numbers.
#
#Joynernacci numbers are similar to Fibonacci numbers, but
#with two differences:
#
# - Fibonacci numbers are famous, Joynernacci numbers are
#   not (yet).
# - In Joynernacci numbers, even-indexed numbers are the
#   sum of the previous two numbers, while odd-indexed
#   numbers are the absolute value of the difference
#   between the previous two numbers.
#
#For example: the Joynernacci sequence starts with 1 and 1
#as the numbers at index 1 and 2. 3 is an odd index, so
#the third number would be 0 (1 - 1 = 0). 4 is an even
#index, so the fourth number would be 1 (0 + 1). 5 is an
#odd index, so the fifth number would be 1 (1 - 0). And
#so on.
#
#The first several Joynernacci numbers (and their indices)
#are thus:
#
# 1  1  0  1  1  2  1  3  2  5  3  8  5 13  8 21 13 34 21
# 1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19
#
#Write a function called joynernacci that returns the nth
#Joynernacci number. For example:
#
# joynernacci(5) -> 1
# joynernacci(12) -> 8
#
#We recommend implementing joynernacci recursively, but it
#is not required.


#Write your code here!
def joynernacci(a_int):
    if a_int > 2 :
        if a_int % 2 == 0:
            return joynernacci(a_int-1) + joynernacci(a_int-2)
        else:
            return abs(joynernacci(a_int-1) - joynernacci(a_int-2))
    else:
        return 1
#Below are some lines of code that will test your function.
#You can change the value of the variable(s) to test your
#function with different inputs.
#
#If your function works correctly, this will originally
#print: 1, then 8
print(joynernacci(5))
print(joynernacci(12))




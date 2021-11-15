#Remember that Fibonacci's sequence is a sequence of numbers
#where every number is the sum of the previous two numbers.
#
#Let's write a variant of Fibonacci's sequence called fib_skip.
#Here, every number will be the sum of the previous number,
#and the number two steps earlier. So, the fourth number is
#the sum of the third and first number; the fifth number is
#the sum of the second and fourth number; and so on.
#
#To do this, we must define the first three numbers of the
#sequence as 1, 1, 1. From there, the sequence continues:
#
# 1, 1, 1, 2, 3, 4, 6, 9, 13, 19, 28...
#
#For example, the last number is 28 because it is the sum
#of the previous number (19) and the number two steps before
#the previous number (9). So, fib_skip(11) = fib_skip(10) +
#fib_skip(8).
#
#Write the function fib_skip using recursion. fib_skip
#takes as input an integer, and returns the fib_skip
#number corresponding to that integer. For example:
#
# - fib_skip(1) = 1
# - fib_skip(2) = 1
# - fib_skip(3) = 1
# - fib_skip(4) = 3
# - fib_skip(9) = 13
# - fib_skip(11) = 28
#
#fib_skip MUST be implemented recursively.
#
#Hint: Think first about how many base cases you have!
#The base cases are the numbers for which the answer
#to fib_skip is _defined_, not _calculated_.


#Write your code here!
def fib_skip(a_int):
    if a_int>3:
        return fib_skip(a_int-1) + fib_skip(a_int-3)
    else:
        return 1

#The lines below will test your code. If your funciton is
#correct, they will print 1, 1, 1, 13, and 28.
print(fib_skip(1))
print(fib_skip(2))
print(fib_skip(3))
print(fib_skip(9))
print(fib_skip(11))



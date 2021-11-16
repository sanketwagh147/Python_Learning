#Remember that Fibonacci's sequence is a sequence of numbers
#where every number is the sum of the previous two numbers.
#
#There exists a variant of Fibonacci's sequence called
#Fibonacci's multiplicative sequence. Fibonacci's
#multiplicative sequence is identical to Fibonacci's
#sequence, except that each number is the PRODUCT of the
#previous two numbers instead of the sum. Let's call these
#FibMult numbers.
#
#In order to make this interesting, we set the first two
#FibMult numbers to 1 and 2. So, the 1st FibMult number is
#1, and the second FibMult number is 2.
#
#So, here are the first few FibMult numbers:
#
#         n  = 1 2 3 4 5  6   7    8       9          10
# FibMult(n) = 1 2 2 4 8 32 256 8192 2097152 17179869184
#
#The sequence gets large fast!
#
#Write the function fib_mult using recursion. fib_mult
#takes as input an integer, and returns the FibMult
#number corresponding to that integer. For example:
#
# - fib_mult(1) = 1
# - fib_mult(2) = 2
# - fib_mult(3) = 2
# - fib_mult(9) = 2097152
# - fib_mult(12) = 618970019642690137449562112
#
#fib_mult MUST be implemented recursively.
#
#Hint: You will actually have two separate base cases,
#one for n = 1 and one for n = 2.


#Write your code here!

def fib_mult(integer):
    if integer > 2:
        return fib_mult(integer-2) * fib_mult(integer-1)
    else:
        if integer > 1:
            return 2
        else:
            return 1

#The lines below will test your code. If your funciton is
#correct, they will print 1, 2, 2, and 2097152.
print(fib_mult(1))
print(fib_mult(2))
print(fib_mult(3))
print(fib_mult(9))



#Write a function that will calculate the Knox index of a
#number. The Knox Index is a thing I made up for this
#problem, and it is defined as follows:
#
#Start with the number. If the number is even, divide it by
#2. If the number is odd, add one. Repeat. Eventually, no
#matter what number you begin with, this sequence will
#converge on 1. If you continue repeating it, you'll repeat
#1-2-1-2 indefinitely.
#
#For example, imagine we started with the number 50:
#50 is even, so 50 / 2 = 25
#25 is odd, so 25 + 1 = 26
#26 is even, so 26 / 2 = 13
#13 is odd, so 13 + 1 = 14
#14 is even, so 14 / 2 = 7
#7 is odd, so 7 + 1 = 8
#8 is even, so 8 / 2 = 4
#4 is even, so 4 / 2 = 2
#2 is even, so 2 / 2 = 1
#
#Starting with 50, this sequence converges on 1 in 9
#iterations: 50 to 25, 25 to 26, 26 to 13, 13 to 14, 14 to
#7, 7 to 8, 8 to 4, 4 to 2, and 2 to 1.
#
#Implement a function called knox. knox should take as
#input an integer, and return the integer's Knox index;
#that is, the number of iterations it takes for the
#number to reach 1 following those rules. For example,
#knox(50) would return 9 because it took 9 iterations to
#converge on 1.


#Add your code here!
def knox(a_int):
    count = 0
    while a_int !=1:
        if a_int %2 == 0:
            a_int /= 2
            count += 1
        else:
            a_int += 1
            count += 1
    return count
#Below are some lines of code that will test your function.
#You can change the value of the variable(s) to test your
#function with different inputs.
#
#If your function works correctly, this will originally
#print: 9, 5, and 8, each on their own lines.
print(knox(50))
print(knox(15))
print(knox(25))





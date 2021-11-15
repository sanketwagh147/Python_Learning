x = 10
y = 5
z = 2

#You may modify the lines of code above, but don't move them!
#When you Submit your code, we'll change these lines to
#assign different values to the variables.
#
#Implement and print out the results of the formula below,
#rounded to two decimal places:
#
# z / (x * y)
#
#When x, y, and z are all numbers, this should work just
#fine: for example, for x = 10, y = 5, and z = 2, this would
#print out 0.04: 2 / (10 * 5) = 0.04.
#
#However, some things might go wrong. The product of x and y
#could be 0, or one of the values could be a string instead of
#a number.
#
#If a divide-by-zero error occurs instead, print the message:
#"Can't divide by zero!" (without the quotation marks).
#
#If one of the values ends up being a string, print the message:
#"Can't divide by a string!" (without the quotation marks).
#
#No matter what happens, your code should print "Done!" (without
#quotation marks) at the end.
#
#Note that you may not use any conditionals in your answer.
#Note also that you should not assume that every error that
#occurs is a divide-by-zero error: any other errors should
#not be caught.


#Add your code here!

try:
    a = z/ (x*y)
    print(round(a, 2))
except ZeroDivisionError:
    print("Can't divide by zero!" )
except TypeError:
    print("Can't divide by a string!")
finally:
    print("Done!")




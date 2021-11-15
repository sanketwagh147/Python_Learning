my_int = 5

#You may modify the lines of code above, but don't move them!
#When you Submit your code, we'll change these lines to
#assign different values to the variables.

#Check to see whether the value of my_int is even or odd, and
#whether it's positive or negative.
#
# - If it's even and positive, print "Evenly positive".
# - If it's even and negative, print "Evenly negative".
# - If it's odd and positive, print "Oddly positive".
# - If it's odd and negative, print "Oddly negative".
#
#You may assume the number will not be 0.

#Add your code here!
a= "Evenly positive"
b= "Evenly negative"
c= "Oddly positive"
d= "Oddly negative"
if my_int > 0:
    print(a) if my_int % 2 == 0 else print(c)
else:
    print(b) if my_int % 2 == 0 else print(d)



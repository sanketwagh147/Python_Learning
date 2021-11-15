minimum = 5
maximum = 10

#You may modify the lines of code above, but don't move them!
#When you Submit your code, we'll change these lines to
#assign different values to the variables.

#Write a loop (we suggest a for loop) that sums all the numbers
#from minimum to maximum, including both minimum and maximum
#themselves. You may assume minimum will always be less than
#maximum.
#
#Your code should not only add the numbers; it should also
#print the current sum after each number is added. So, for
#minimum = 5 and maximum = 10, your code would print the results
#of adding 5 + 6 + 7 + 8 + 9 + 10:
#5
#11
#18
#26
#35
#45
a_list = list(range(minimum, maximum+1))
a_list.insert(0,0)
print(a_list)
a = 0
for i in range(0 , maximum- minimum+1):

    x = a_list[i]
    # print(x,"x")
    y = a_list[i+1]
    # print(y,"y")
    a=+ a + y
    print(a)

    

#Add your code here!


a_list = [1,2,3]
b_list = [40,44,45]
def add1(a,b):
    sum1 = a+b
    return sum1
#use the map function to pass 2 parameters and operete a single function.
print(add1(1,3))
c_list=list(map(add1, a_list, b_list))  # To make new list we need to use the list function
print(c_list)

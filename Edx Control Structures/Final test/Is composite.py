#Write a function called is_composite. is_composite should
#take as input one integer. It should return True if the
#integer is composite, False if the integer is not not
#composite. You may assume the integer will be greater than
#2 and less than 1000.
#
#Remember, a composite number is one into which at least
#one number is divisible besides 1 and the number itself.
#For example, 6 is composite because it is divisible by 2
#and 3. 7 is not composite because it is only divisible by 1
#and itself.
#
#HINT: Remember, once you find a _single_ factor of the
#number, you can return True: it only takes one factor
#to make the number composite.


#Add your code here!
div_list = list(range(1, 100))
# print(div_list)
factor_list = []
def is_composite(a_integer):
    factor_list = []
    for each in div_list:
        if a_integer % each == 0:
            factor_list.append(each)
    # print(factor_list)
    if len(factor_list) >= 3:
        return True
    else:
        return False

#Below are some lines of code that will test your function.
#You can change the value of the variable(s) to test your
#function with different inputs.
#
#If your function works correctly, this will originally
#print: False, True, False, True, False, True
print(is_composite(5))
print(is_composite(6))
print(is_composite(97))
print(is_composite(105))
print(is_composite(997))
print(is_composite(999))
# #






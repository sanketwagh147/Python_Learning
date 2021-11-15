#The Greatest Common Factor (GCF) of two numbers is the
#largest number that divides evenly into those two
#numbers. For example, the Greatest Common Factor of 48
#and 18 is 6. 6 is the largest number that divides evenly
#into 48 (48 / 6 = 8) and 18 (18 / 6 = 3).
#
#Write a function called find_gcf. find_gcf should have
#two parameters, both integers. find_gcf should return
#the greatest common factor of those two numbers.
#
#For example:
#
# find_gcf(48, 18) -> 6
# find_gcf(21, 7) -> 7
# find_gcf(47, 17) -> 1
#
#If one number is a multiple of the other, the greatest
#common factor is the smaller number (e.g. 21 and 7). If
#the numbers have no common factors, then their greatest
#common factor is 1 (e.g. 47 and 17).


#Write your function here!
def find_HCF(a,b):
    fact_a =[]
    fact_b =[]
    for i in range(1, 1000):
        if a % i == 0:
            fact_a.append(i)
        if b % i == 0:
            fact_b.append(i)
    # print(fact_a)
    # print(fact_b)
    set1 = set(fact_a)
    intersection = set1.intersection(fact_b)
    return max(intersection)

def find_gcf(int_1, int_2):
    f_div = int_1/int_2
    s_div = int_2/int_1
    # print(f_div, s_div)
    if f_div.is_integer() or s_div.is_integer():
        return min(int_1,int_2)
    else:
        return  find_HCF(int_1,int_2)
    # elif
    #
    # else:
    #     return 1


#The lines below will test your code. Feel free to modify
#them. If your code is working properly, these will print
#the same output as shown above in the examples.
print(find_gcf(48, 18))
print(find_gcf(21, 7))
print(find_gcf(47, 17))



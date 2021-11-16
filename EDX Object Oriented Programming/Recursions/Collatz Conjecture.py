# def collatz(a_int):
#     print(a_int)
#     if a_int % 2 == 0:
#         return collatz(a_int//2)
#     elif a_int %2 ==1:
#         return collatz(a_int*3 + 1)
#     else:
#         return collatz(a_int*3+1)
#
# collatz(17)


def collatz(current_number):
    # print(current_number)
    count = 0
    while current_number != 1:
        count += 1
        if current_number % 2 == 0:
            current_number = (current_number // 2)
        else:
            current_number = (current_number * 3+1)
    else:
        return count
print(collatz(23))

"""
Exercise R-1.4
Exercise R-1.5
find sum of square of positive int in smaller than n 
"""

from icecream import ic


def sum_square_positive_int(num: int) -> int:

    sum = 0
    for i in range(1, num + 1):

        # even no
        if i % 2 == 0:
            sum += i * i

    return sum


if __name__ == "__main__":
    ic(sum_square_positive_int(12))
    ic(sum_square_positive_int(5))

    # R-1.5
    num = 10
    ic(sum([i * i for i in range(1, num + 1) if i % 2 == 0]))
    num = 12
    ic(sum([i * i for i in range(1, num + 1) if i % 2 == 0]))
    num = 5
    ic(sum([i * i for i in range(1, num + 1) if i % 2 == 0]))

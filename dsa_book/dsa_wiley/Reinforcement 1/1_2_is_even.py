"""
Exercise 1.2
"""

from icecream import ic


def is_even(num: int) -> bool:

    while num > 0:
        # subtract 2
        num -= 2

    # if even num -> 0 else -1
    return num == 0


if __name__ == "__main__":
    ic(is_even(2))
    ic(is_even(23))
    ic(is_even(28))

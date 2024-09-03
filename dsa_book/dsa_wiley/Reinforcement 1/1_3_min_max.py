"""
Exercise 1.3
"""

from collections import namedtuple

from icecream import ic

# ! namedtuple example
MinMax = namedtuple("MinMax", ("min", "max"))


def get_min_max(a: int, b: int, *args: int) -> MinMax:

    # ! args example
    sequence = [a, b] + [*args]
    min_ = sequence[0]
    max_ = sequence[0]

    # ic(sequence)
    for val in sequence:
        if val < min_:
            min_ = val

        if val > max_:
            max_ = val

    return MinMax(min=min_, max=max_)


if __name__ == "__main__":
    ic(get_min_max(1, 2, 18, 123))
    ic(get_min_max(1212, 22, 18, 23, 231, 11))
    ...

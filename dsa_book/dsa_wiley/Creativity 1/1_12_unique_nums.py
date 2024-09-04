"""
C-1.12
get unique nums count
"""

from icecream import ic


def get_unique_int(seq: list[int]) -> int:
    unique_nums = []
    for each in seq:
        if each not in unique_nums:
            unique_nums.append(each)

    return len(unique_nums)


if __name__ == "__main__":
    ic(get_unique_int([1, 2, 3, 3, 4, 5, 5]))

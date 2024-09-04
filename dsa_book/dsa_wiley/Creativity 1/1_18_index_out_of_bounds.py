from typing import Any

from icecream import ic


def index_out_of_bound(seq1: list, index_: int, val: Any):

    shallow_copy = list(seq1)

    try:
        shallow_copy[index_] = val
    except IndexError as exc:
        ic(exc)
        ic("Don't try overflow attacks in python lol")
    return shallow_copy


if __name__ == "__main__":
    # ic(index_out_of_bound([1, 2, 3], 4, 100))
    ic(index_out_of_bound([1, 2, 3], 0, 100))

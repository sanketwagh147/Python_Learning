"""
C-1.11
input:
    seq[int]
if seq[0] != seq[1] ->  seq[0] * seq[1]  == even

Determine distinct pairs whose product is even
"""

from typing import Sequence

from icecream import ic


def distinct_consecutive_pair_with_even_product(seq: Sequence[int]) -> bool:

    for i in range(len(seq) - 1):
        pair = (seq[i], seq[i + 1])
        ic(pair)
        if pair[0] != pair[1]:
            pair_product = pair[0] * pair[1]
            ic(pair_product)

            is_pair_product_even = pair_product % 2 == 0

            if is_pair_product_even:
                return is_pair_product_even

    return False


if __name__ == "__main__":
    ic(distinct_consecutive_pair_with_even_product([3, 5, 3, 1]))

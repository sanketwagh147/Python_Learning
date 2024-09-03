"""
C-1.10
Custom reverse
"""

from typing import Sequence, TypeVar

from icecream import ic

SeqItem = TypeVar("SeqItem")


def rev_seq(seq: Sequence[SeqItem]) -> Sequence:
    return seq[::-1]


if __name__ == "__main__":
    ic(rev_seq([1, 4, 51, 123]))

import random
from typing import Sequence, TypeVar

from icecream import ic

#

# Type  Var usage
SeqItem = TypeVar("SeqItem")


def rand_choice_using_rand_range(
    seq: Sequence[SeqItem],
) -> SeqItem:
    return seq[random.randrange(len(seq))]


if __name__ == "__main__":
    ic(rand_choice_using_rand_range(["a", "b", "c", "d"]))
    ic(rand_choice_using_rand_range(["p", "q", "r", "s"]))
    var = ic(rand_choice_using_rand_range(["l", "m", "n", "o"]))
    ic(var)

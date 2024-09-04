import random
from string import ascii_lowercase

from icecream import ic


def shuffle_with_randint(seq: list) -> list:

    rand_seq = []

    while len(seq) != len(rand_seq):

        rand_index = random.randint(0, len(seq) - 1)

        if rand_index not in rand_seq:
            rand_seq.append(rand_index)

        # ic(rand_index)

    return [seq[i] for i in rand_seq]


if __name__ == "__main__":
    # ic(shuffle_with_randint(["a", "b", "c", "d"]))
    # ic(shuffle_with_randint(list(ascii_lowercase)))
    # a = shuffle_with_randint(list(ascii_lowercase))
    # a.sort()
    # ic(a)
    ic(sorted(shuffle_with_randint(list(ascii_lowercase))) == list(ascii_lowercase))

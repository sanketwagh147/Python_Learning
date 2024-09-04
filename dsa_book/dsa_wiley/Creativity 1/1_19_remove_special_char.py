from string import ascii_letters
from typing import Any

from icecream import ic


def remove_special_char(sentence: str):
    chr_set = list(ascii_letters) + [str(i) for i in range(10)] + [" "]

    return "".join([chr for chr in sentence if chr in chr_set])


if __name__ == "__main__":
    # ic(index_out_of_bound([1, 2, 3], 4, 100))
    ic(remove_special_char("Hello ! This is sanket's code ?"))

# WAP to find frequency of each element in array
from icecream import ic


def find_freq(arr: list):
    frequencies = {}

    for item in arr:

        if item not in frequencies.keys():
            frequencies[item] = 1
        else:
            frequencies[item] += 1

    return frequencies


if __name__ == "__main__":
    foo = [1, 2, 3, 3, 4]

    ic(find_freq(foo))

    ...

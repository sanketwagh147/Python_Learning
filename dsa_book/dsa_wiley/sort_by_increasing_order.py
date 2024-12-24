# WAP to sort by increasing order

from dsa_book.dsa_wiley.find_freq import find_freq


def sort_by_increasing_order(arr: list):

    frequencies = find_freq(arr)
    sorted_tuple = sorted(frequencies.items(), key=lambda item: item[1])
    # print(sorted_tuple)

    # ret = []

    # for each in sorted_tuple:
    #     ret.extend([each[0]] * each[1])

    return [each[0] for each in sorted_tuple for _ in range(each[1])]


if __name__ == "__main__":
    lst = [6, 6, 6, 6, 6, 6, 1, 2, 3, 3, 3, 2, 4, 4, 4, 4, 4]
    print(sort_by_increasing_order(lst))

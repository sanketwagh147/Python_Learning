from dsa_book.dsa_wiley.find_freq import find_freq

# WAP to remove max frequ


def remove_max_freq(arr: list):

    frequencies = find_freq(arr)
    max_freq = 0
    item_most_repeated = -1

    for each in frequencies.keys():
        if frequencies[each] > max_freq:
            max_freq = frequencies[each]
            item_most_repeated = each

    for i in range(max_freq):
        arr.remove(item_most_repeated)

    return arr


if __name__ == "__main__":
    foo = [1, 1, 2, 2, 3, 3, 4, 4, 4, 4, 5, 6, 6]
    foo1 = [1, 1, 2, 2, 3, 3, 4, 4, 4, 4, 5, 6, 6, 6, 6, 6, 6]
    # print(remove_max_freq(foo))
    print(remove_max_freq(foo1))

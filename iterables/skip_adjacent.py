"""
Sort the array and skip the element if it is similar and adjacent


"""

candidates = [10, 10, 1, 2, 7, 6, 1, 5]


def skip_adjacent(arr):
    arr.sort()
    res = []
    prev = -1
    for i in range(0, len(candidates)):
        # Skip duplicates
        if candidates[i] == prev:
            continue

        res.append(candidates[i])
        prev = candidates[i]

    return res


if __name__ == "__main__":
    print(skip_adjacent(candidates))

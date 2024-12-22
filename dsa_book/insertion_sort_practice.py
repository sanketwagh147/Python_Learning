from icecream import ic


def insertion_sort(arr):
    n = len(arr)

    if n in (0, 1):
        return arr

    for i in range(n):

        current = arr[i]

        j = i

        while j > 0 and arr[j - 1] > current:

            arr[j] = arr[j - 1]

            j -= 1

        arr[j] = current

    return arr


if __name__ == "__main__":
    case1 = []
    case2 = [1]
    case3 = [4, 5]
    case4 = [5, 4]
    case5 = [1, 6, 4, 2, 5]
    case6 = [6, 6, 2, 8, 7, 8]

# ic(insertion_sort(case4))
ic(insertion_sort(case5))
ic(insertion_sort(case6))

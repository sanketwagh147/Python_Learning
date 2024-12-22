from icecream import ic


def insertion_sort(array: list):
    ic(array)

    num_items = len(array)
    # No need to sort if array is empty or hast just 1 item
    if len(array) in (0, 1):
        return array

    # loop from  second item
    for i in range(1, num_items):

        curr = array[i]
        j = i

        while j > 0 and array[j - 1] > curr:
            ic(array[j - 1], curr, "-> Comparison")

            ic(i, j, array[i], array[j])

            array[j] = array[j - 1]
            ic(array[j], "<->", array[j - 1])
            j -= 1

        array[j] = curr

    return array


if __name__ == "__main__":
    case1 = []
    case2 = [1]
    case3 = [4, 5]
    case4 = [5, 4]
    case5 = [1, 6, 4, 2, 5]
    case6 = [6, 6, 2, 8, 7, 8]

# ic(insertion_sort(case4))
ic(insertion_sort(case5))

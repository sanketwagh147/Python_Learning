# WAP to pop right element of the given from array


def pop_right(arr: list, item):

    # find the index
    # If not found raise exception

    try:
        item_inx = arr.index(item)
    except ValueError as exc:
        raise ValueError("Item not found") from exc
    else:
        try:
            arr.pop(item_inx + 1)
        except IndexError as exc:
            raise IndexError("popped item is on extreme right thus cant pop") from exc

        return arr

    # pop index + 1


if __name__ == "__main__":
    foo = [1, 23, 123, 123123, 111]
    print(pop_right(foo, 23))
    # print(pop_right(foo, 13))
    print(pop_right(foo, 111))

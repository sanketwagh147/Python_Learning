from icecream import ic


def can_divide_by_2(num: int, divide_count=1):

    # if num <= 2:
    #     return divide_count

    # else:
    #     num = num / 2
    #     ic(num)
    #     divide_count += 1

    #     can_divide_by_2(num, divide_count=divide_count)

    # return divide_count
    count = 0
    # ic(num, count)
    while num >= 2:
        num = num / 2
        # ic(num)
        count += 1

    return count


if __name__ == "__main__":
    for x in range(3, 100):
        print(can_divide_by_2(x), end=", ")
    # ic(can_divide_by_2(187))

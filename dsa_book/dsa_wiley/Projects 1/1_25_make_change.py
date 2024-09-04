from icecream import ic

denominations: list[int] = [1, 2, 5, 10, 20, 50, 100, 500, 2000]


def make_change(given: int, charged: int):
    change = {}

    difference = given - charged

    ic(difference)

    for each in sorted(denominations, reverse=True):

        if difference >= each:
            count_of_cur_curency = difference // each
            difference = difference % each

            if count_of_cur_curency:
                change[each] = count_of_cur_curency

    if difference < 1:
        change[difference] = 1

    return change


if __name__ == "__main__":
    given = 1241.25
    charged = 1124.21
    ch = make_change(given, charged)
    ic(ch)
    chn_amoutn = 0
    for each, val in ch.items():
        chn_amoutn += each * val
    ic(chn_amoutn == (given - charged))

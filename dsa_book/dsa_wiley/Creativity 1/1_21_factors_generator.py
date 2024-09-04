from icecream import ic


def factors(n: int):
    k = 1

    while k * k < n:
        if n % k == 0:
            yield k
            yield n // k
        k += 1

    if k * k == n:
        yield k


def factors_ordered(n: int):
    # First, yield small factors

    sqr_root = int(n**0.5)
    ic(sqr_root)

    # l_small = list(range(1, sqr_root + 1))
    # ic(l_small)
    # first divide by small
    for k in range(1, sqr_root + 1):
        if n % k == 0:
            yield k

    # Then, yield large factors in reverse order
    l_lit = list(range(sqr_root, 0, -1))

    # ic(l_lit)
    for k in range(int(n**0.5), 0, -1):
        if n % k == 0 and k != n // k:  # Avoid duplicates
            yield n // k


if __name__ == "__main__":
    # ic(list(factors(100)))
    ic(list(factors_ordered(100)))
    # gen = factors_ordered(100)
    # ic(next(gen))
    # ic(next(gen))

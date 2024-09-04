from icecream import ic


def get_euclidean_norm(seq: list, p: int = 2):
    return sum([i**p for i in seq]) ** (1 / p)


if __name__ == "__main__":
    ic(get_euclidean_norm([4, 3]))
    ic(get_euclidean_norm([4, 3, 4, 5], 3))

from icecream import ic


def arr_dot_prod(seq1: list, seq2: list):

    return sum([seq1[i] * seq2[i] for i in range(len(seq1))])


if __name__ == "__main__":
    ic(arr_dot_prod([1, 2, 3], [3, 2, 1]))

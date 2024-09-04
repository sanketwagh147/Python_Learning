from icecream import ic


def main():
    inp = input("Enter 3 ints divided by space : ")
    inp = inp.split(" ")
    inputs = []
    for each in inp:
        try:
            inputs.append(int(each))
        except ValueError as exc:
            # ic(exc)
            inputs.append(each)
    a, b, c = [*inputs]

    try:
        _ = a + b
    except TypeError as exc:
        ic(exc)
        ic("Plus operation not  allowed with given input types:")

    try:
        _ = b - c
    except TypeError as exc:
        ic(exc)
        ic("minus operation not  allowed with given input types")
    try:

        _ = a * b
    except TypeError as exc:
        ic(exc)
        ic("Mul operation not  allowed with given input types")

    ic("SUCCESS")


if __name__ == "__main__":
    main()

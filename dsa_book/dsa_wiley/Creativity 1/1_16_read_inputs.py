from icecream import ic


def input_printer():
    inputs = []
    while True:
        try:
            text = input("Enter the text: ")
            inputs.append(text)
        except EOFError as exc:
            ic(exc)
            break

    for each in reversed(inputs):
        ic(each)


if __name__ == "__main__":
    input_printer()

result = 0
past_comman = None
while True:

    try:
        curr_input = input("inp: ")

        commands = ["+", "-", "*", "/", "clear"]

        if curr_input in commands:
            if curr_input == "clear":
                result = 0
            past_comman = curr_input

        else:
            if past_comman is None:
                result = int(curr_input)
            if past_comman == "+":
                result += int(curr_input)
            elif past_comman == "-":
                result -= int(curr_input)
            elif past_comman == "*":
                result *= int(curr_input)
            elif past_comman == "/":
                result /= int(curr_input)
        print(result)

    except EOFError as exc:
        print(exc)
        break

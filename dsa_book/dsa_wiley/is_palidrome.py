def is_palindrome(inp_str: str):

    len_inp_str = len(inp_str)

    for i in range(len_inp_str // 2):
        print(i, inp_str[i])
        if inp_str[i] != inp_str[-1 - i]:
            return False

    return True


if __name__ == "__main__":
    print(is_palindrome("abbba"))

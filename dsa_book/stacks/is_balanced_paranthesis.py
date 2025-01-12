class Stack:
    def __init__(self):
        self.stack_list = []

    def print_stack(self):
        for i in range(len(self.stack_list) - 1, -1, -1):
            print(self.stack_list[i])

    def is_empty(self):
        return len(self.stack_list) == 0

    def peek(self):
        if self.is_empty():
            return None
        else:
            return self.stack_list[-1]

    def size(self):
        return len(self.stack_list)

    def push(self, value):
        self.stack_list.append(value)

    def pop(self):
        if self.is_empty():
            return None
        else:
            return self.stack_list.pop()


k = "asdf"


def is_balanced_parentheses(txt: str):

    stack = Stack()
    matching_pairs = {")": "("}

    for ch in txt:

        # push opening brackets in stack
        if ch in matching_pairs.values():
            stack.push(ch)
        # if closing brackets
        elif ch in matching_pairs.keys():  # Closing parentheses

            if stack.is_empty() or stack.peek() != matching_pairs[ch]:
                return False
            stack.pop()

    return stack.is_empty()


def test_is_balanced_parentheses():
    try:
        assert is_balanced_parentheses("((()))") == True
        print("Test case 1 passed")
    except AssertionError:
        print("Test case 1 failed")

    try:
        assert is_balanced_parentheses("()") == True
        print("Test case 2 passed")
    except AssertionError:
        print("Test case 2 failed")

    try:
        assert is_balanced_parentheses("(()())") == True
        print("Test case 3 passed")
    except AssertionError:
        print("Test case 3 failed")

    try:
        assert is_balanced_parentheses("(()") == False
        print("Test case 4 passed")
    except AssertionError:
        print("Test case 4 failed")

    try:
        assert is_balanced_parentheses("())") == False
        print("Test case 5 passed")
    except AssertionError:
        print("Test case 5 failed")

    try:
        assert is_balanced_parentheses(")(") == False
        print("Test case 6 passed")
    except AssertionError:
        print("Test case 6 failed")

    try:
        assert is_balanced_parentheses("") == True
        print("Test case 7 passed")
    except AssertionError:
        print("Test case 7 failed")

    try:
        assert is_balanced_parentheses("()()()()") == True
        print("Test case 8 passed")
    except AssertionError:
        print("Test case 8 failed")

    try:
        assert is_balanced_parentheses("(())(())") == True
        print("Test case 9 passed")
    except AssertionError:
        print("Test case 9 failed")

    try:
        assert is_balanced_parentheses("(()()())") == True
        print("Test case 10 passed")
    except AssertionError:
        print("Test case 10 failed")

    try:
        assert is_balanced_parentheses("((())") == False
        print("Test case 11 passed")
    except AssertionError:
        print("Test case 11 failed")


test_is_balanced_parentheses()

# print(is_balanced_parentheses(")("))

"""
Sample implementation of an adapter patter
Here we can see we have methods defined as per our naming and additional function
"""


class EmptyException(Exception): ...


class ArrayStack:
    """
    LIFO stack using python list
    """

    def __init__(self) -> None:
        self._data = []

    def __len__(self):
        return len(self._data)

    def is_empty(self):
        return len(self._data) == 0

    def push(self, e):
        self._data.append(e)

    def top(self):
        if self.is_empty():
            raise EmptyException
        return self._data[0]

    def pop(self):
        if self.is_empty():
            raise EmptyException
        return self._data.pop()

    def __str__(self) -> str:
        return f"<ArrayStack {str(self._data)}>"


if __name__ == "__main__":
    arr_stack = ArrayStack()
    arr_stack.push(1)
    arr_stack.push(1)
    arr_stack.push(1)
    arr_stack.push(1)
    print(arr_stack)
    arr_stack.push(2)
    arr_stack.pop()
    print(arr_stack)

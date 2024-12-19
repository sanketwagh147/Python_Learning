from collections.abc import Sequence


class MySequence(Sequence):
    def __init__(self, data):
        self._data = list(data)

    def __getitem__(self, index):
        return self._data[index]

    def __len__(self):
        return len(self._data)

    # Lexicographical comparison: self <= other
    def __le__(self, other):
        if not isinstance(other, Sequence):
            return NotImplemented
        return list(self._data) <= list(other)


# Example usage
seq1 = MySequence([1, 2, 3])
seq2 = MySequence([1, 2, 4])
seq3 = MySequence(["a", "b", "c"])
seq4 = MySequence(["a", "b", "c"])

# print(seq1 <= seq2)  # True, since [1, 2, 3] <= [1, 2, 4]
print(seq3 <= seq4)

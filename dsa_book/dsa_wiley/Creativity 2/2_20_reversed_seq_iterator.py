from icecream import ic


class SequenceIterator:
    def __init__(self, sequence):
        self._seq = sequence
        self._k = -1

    def __next__(self):
        self._k += 1
        if self._k < len(self._seq):
            return self._seq[self._k]
        else:
            raise StopIteration()

    def __iter__(self):
        return self


class ReverseSequenceIterator:
    def __init__(self, sequence):
        self._seq = sequence
        self._k = len(sequence)

    def __next__(self):
        self._k -= 1
        if self._k >= 0:
            # ic(self._k)
            return self._seq[self._k]
        else:
            raise StopIteration()

    def __iter__(self):
        return self


if __name__ == "__main__":
    rseq = ReverseSequenceIterator([10, 2, 3, 4])
    ic(next(rseq))
    ic(next(rseq))
    ic(next(rseq))
    ic(next(rseq))

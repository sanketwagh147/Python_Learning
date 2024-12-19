from icecream import ic


class Progression:

    def __init__(self, start=0) -> None:
        self._current = start

    def _advance(self):
        self._current += 1

    def __next__(self):
        if self._current is None:
            raise StopIteration()
        else:
            answer = self._current
            self._advance()
            return answer

    def __iter__(self):
        """
        By Convention iterator must return itself as an iterator
        """
        return self

    def print_progression(self, n):
        print(" ".join(str(next(self)) for j in range(n)))


class ArithmeticProgression(Progression):
    def __init__(self, increment=1, start=0) -> None:
        super().__init__(start)
        self._increment = increment

    def _advance(self):
        self._current += self._increment


if __name__ == "__main__":
    ap = ArithmeticProgression(128)
    # ic(next(ap))
    # ic(next(ap))
    # ic(next(ap))
    count = 0
    result = 0
    while result < 2**63:
        result = next(ap)
        ic(result)
        count += 1
    else:
        print(f"Times : {count}")

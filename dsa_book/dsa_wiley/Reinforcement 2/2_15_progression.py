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


class FibonacciProgression(Progression):

    def __init__(self, first=0, second=1) -> None:
        self._current = first  # 0
        self._previous = second - first  # 1

    def __next__(self):
        # ic(self._current)
        # ic(self._previous)
        answer = self._current

        self._current, self._previous = (
            self._current + self._previous,
            self._current,
        )
        return answer

    def __getitem__(self, item):
        current, previous = self._current, self._previous

        for i in range(item + 1):
            answer = next(self)

        self._current, self._previous = current, previous

        return answer


if __name__ == "__main__":
    f = FibonacciProgression(2, 2)
    f2 = FibonacciProgression()
    # for i in range(8):
    #     print(f"Value number {i+1} is {f[i]}")
    f.print_progression(8)
    f2.print_progression(10)

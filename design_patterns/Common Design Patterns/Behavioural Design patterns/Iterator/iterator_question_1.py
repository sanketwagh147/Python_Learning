


class CountUp():
    def __init__(self, start: int = 0, end: int = 10, step: int = 1) -> None:
        if step == 0:
            raise ValueError("step must not be 0")

        self.start = start
        self.end = end
        self.step = step
        self.current = self.start

    def __iter__(self) -> "CountUp":
        return self

    def __next__(self) -> int:
        if self.step > 0 and self.current >= self.end:
            raise StopIteration

        if self.step < 0 and self.current <= self.end:
            raise StopIteration

        current = self.current
        self.current += self.step
        return current

if __name__ == "__main__":
    counter = CountUp(1, 10, 2)
    for num in counter:
        print(num)
    # → 1, 3, 5, 7, 9

    print(list(CountUp(0, 5, 1)))  # → [0, 1, 2, 3, 4]
    print(list(CountUp(10, 0, -2)))  # → [10, 8, 6, 4, 2]

    c = CountUp(10, 15, 3)
    print(next(c))  # → 10
    print(next(c))  # → 13
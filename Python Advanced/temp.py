class FooDecorator:
    def __init__(self, func) -> None:
        self.func = func
        self.call_count = 0

    def __call__(self, *args, **kwargs):

        print("Before calling the function")
        result = self.func(*args, **kwargs)
        print("After calling the function")
        self.call_count += 1
        print(self.call_count)
        return self.func()


@FooDecorator
def bar():
    print("running bar")


if __name__ == "__main__":
    bar()
    bar()
    bar()
    bar()
    bar()

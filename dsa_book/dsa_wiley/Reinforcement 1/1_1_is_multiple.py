"""
Exercise 1
"""

from icecream import ic
from test_static_method_import import StaticMethodUsage as sm


def is_multiple(a: int, b: int):
    # ? Why is this required

    if b // a == 0:
        return True

    return False


def test_is_multiple():
    assert is_multiple(15, 3)
    assert not is_multiple(3, 15)


if __name__ == "__main__":
    ic(sm.some_static_method("alsdfjaldj", "alsdjflj"))

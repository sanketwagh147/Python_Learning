"""
Simple decorator which when added will disable the print statements 
"""

import functools
import io
import sys


class NullWriter:
    """ """

    def write(self, _): ...

    def flush(self): ...


def disable_print(func):
    """
    Decorator that disables print statements inside a function.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        disable = kwargs.pop("disable_print", False)  # Extract disable_print flag

        if disable:
            std_out = sys.stdout  # Save current stdout
            sys.stdout = io.StringIO()  # Redirect stdout to suppress output

            try:
                return func(*args, **kwargs)  # Call the function with updated kwargs
            finally:
                sys.stdout = std_out  # Restore stdout
        else:
            return func(*args, **kwargs)  # Call normally if disable_print is False

    return wrapper


class DisablePrint:
    """
    when added will disable print for all child class method
    """

    def __init_subclass__(cls, **kwargs):
        """Automatically decorates all methods in subclasses"""
        super().__init_subclass__(**kwargs)

        for attr_name, attr_value in cls.__dict__.items():
            if callable(attr_value):  # If it's a method
                setattr(cls, attr_name, disable_print(attr_value))


if __name__ == "__main__":
    # usage

    class Foo(DisablePrint):

        def foo(self):
            print("I am just a foo")

        def bar(self):
            print("I am just a bar")

    ob = Foo()
    ob.foo()
    ob.bar()

    print("disabled print")
    ob.foo(disable_print=True)  # type: ignore (this gets dynamically added)
    ob.bar(disable_print=True)  # type: ignore (this gets dynamically added)

"""
Simple decorator which when added will disable the print statements 
"""

import functools
import sys


class NullWriter:
    """ """

    def write(self, _): ...

    def flush(self): ...


def disable_print(func):
    """
    Decorator which disables print
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        std_out = sys.stdout
        sys.stdout = NullWriter()

        try:
            result = func(*args, *kwargs)
        finally:
            sys.stdout = std_out

        return result

    return wrapper

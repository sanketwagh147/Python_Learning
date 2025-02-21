"""
Singleton Decorator
"""

from functools import wraps


def singleton(cls):
    instances = {}

    @wraps(cls)  # Preserve class metadata
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class SingletonClass:
    """A simple Singleton class"""

    pass


obj1 = SingletonClass()
obj2 = SingletonClass()

# print(obj1 is obj2)  # Output: True
# print(SingletonClass.__name__)  # Output: SingletonClass
# print(SingletonClass.__doc__)  # Output: A simple Singleton class

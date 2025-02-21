"""
Singleton Class 
"""


class singleton:
    # private class attribute to hold the instance
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:  # check if instance exists
            cls._instance = super().__new__(cls)
        return cls._instance  # return the single instance


class foo(singleton):

    def fun_foo(self):
        print("running fun_foo")


# usage
obj1 = singleton()
obj2 = singleton()
print(obj1 is obj2)  # output: true (both variables point to the same instance)

foo1 = foo()
foo2 = foo()

print(foo1 is foo2)  # output: true (both variables point to the same instance)

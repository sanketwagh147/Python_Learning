

class StaticMethodUsage:
    
    def __init__(self,foo,bar) -> None:
        self.foo = foo
        self.bar = bar

    @staticmethod
    def some_static_method(blah, blah2):
        return blah + blah2
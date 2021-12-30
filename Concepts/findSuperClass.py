

# finding the super class


class Test:
    pass


class Test2(Test):

    def __init__(self):
        print("Initialized Test2 Obj")

class Test3(Test2):

    def __init__(self):
        print("Initialized Test2 Obj")

class Test3(Test3):

    def __init__(self):
        print("Initialized Test2 Obj")

class Test4(Test3):

    def __init__(self):
        print("Initialized Test2 Obj")

class Test5(Test4):

    def __init__(self):
        print("Initialized Test2 Obj")

obj = Test5()


print(Test5.__base__)
print(Test5.__base__)
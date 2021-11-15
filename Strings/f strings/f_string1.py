def tester(start):
    state = 1
    def nested(label):
        nonlocal state
        state = 0
        print(label, state)
    return nested

f = tester(0)
c = f("s")
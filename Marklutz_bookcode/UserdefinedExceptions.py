# Define a user defined exception
class UserdefinedException(Exception):
    print("test exception")
    pass

# Function to raise a error
def test():
    raise UserdefinedException("test exception from test")

# Try catch block
try:
    test()
except UserdefinedException:
    print("User defined exception passed through except")
finally:
    test()  # raise error  intentionally to check error.
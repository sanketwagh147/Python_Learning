# Basic assert examples

def test(a,b):
    assert a>0, "A mush not be negative"
    assert b>0, "B mush not be negative"
    a,b
    print("a", a)
    return "Assertion succesfully"


# # a is -ve
# a_neg =test(-1, 2)
# print("a_neg", a_neg)

# # b is -ve
# a_neg =test(1, -2)
# print("a_neg", a_neg)


# both positive
a_neg =test(1, 2)
print("a_neg", a_neg)
# This will search the index or position of the target in the list
def linear_search(listy , target):
    """
    :param listy: search the list
    :param target: target to be found
    :return: returns the position of the target if found
    """
    for i in range(0, len(listy)):
        if listy[i] == target:
            return i
    return -1

listy = [1, 2, 5 , 6, 90 , 8398, 1948, 47342, 34, 438]
print(linear_search(listy, 438))

def verify(index):
    if index is not None:
        print("Target found at index: ', index")
    else:
        print("Target Not found")

numbers = list(range(0, 11))

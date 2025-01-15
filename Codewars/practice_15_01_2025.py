"""
Write a function that takes two arguments: an array and a callback function

The function should return true if the callback / block returns false for all of the items in the array, or if the array is empty; otherwise return false.
"""


def cb_returns_False(cb, *arr: list):
    """
    -> True ( cb(item in arr) -> False)
            len(arr) == 0
    -> else False

    """
    if len(arr) == 0:
        return True

    for each in arr:
        cb_r = cb(each)
        if cb_r:
            return False

    return True


def main_cb_returns_false():
    def cb(x):
        if x in (1, 2):
            return True
        return False


    temp_list = [1, 2, 3, 4]

    print(cb_returns_False(cb, temp_list))

if __name__ == "__main__": 
    # main_cb_returns_false()

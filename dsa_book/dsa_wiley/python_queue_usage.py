import math
from queue import LifoQueue

"""
Given array of integer elements:
arr = [ 1,2,3,4,5,5,6,6,8,6]
sum of consecutive pairs 
1+2 = 3
2+3 = 5 ....
# return the the loweset sum
"""


def min_pair_sum(input_list: list):
    print("running")
    queue = LifoQueue()
    for num in input_list:
        queue.put(num)

    min_value = math.inf

    for i in range(len(input_list) - 1):
        print(queue.queue)
        n1 = queue.get()
        print(queue.queue)
        n2 = queue.get()
        queue.put(n2)
        min_value = min(min_value, n1 + n2)
        print
    print("ended")
    return min_value


if __name__ == "__main__":
    print(min_pair_sum([10, 20, 30, 40, 50]))

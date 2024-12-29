"""
Given:
array -> len(array) = n
find consecutive which are less than or greater than
ex:
arr = [ 1,3,4,5]
1,3 - f
3,4 - t
4,5 = t
"""

from queue import Queue


def get_successive_pairs(inp_li: list):
    queue = Queue()
    result = []

    # populate # FIFO queue
    for num in inp_li:
        queue.put(num)

    for i in range(len(inp_li) - 1):
        print(queue.queue)
        num_1 = queue.get()
        print(queue.queue)
        num_2 = queue.get()
        print(queue.queue)
        queue.put(num_2)
        print(queue.queue)
        if abs(num_1 - num_2) == 1:
            result.append((num_1, num_2))

    return result


if __name__ == "__main__":
    print(get_successive_pairs([2, 3, 2, 4, 5, 6, 1, 0]))

def binary_search(listy, target):
    """

    :param listy: Search this list
    :param target: search this item
    :returns index location of the target item if found else returns -1
    """
    first = 0
    last = len(listy)-1
    count = 0
    while first<= last:
        count += 1
        midpoint = (first + last)//2
        if listy[midpoint] == target:
            return midpoint,count
        elif listy[midpoint]< target:
            first = midpoint + 1
        else:
            last = midpoint - 1
    return -1
listy = list(range(0, 100))
print(binary_search(listy, 49))

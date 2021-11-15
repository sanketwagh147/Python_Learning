#Without the explanatory comments, Mergesort is much shorter:

def mergesort(lst):
    if len(lst) <= 1:
        return lst

    else:
        midpoint = len(lst) // 2
        left = mergesort(lst[:midpoint])
        right = mergesort(lst[midpoint:])

        newlist = []
        while len(left) > 0 and len(right) > 0:
            if left[0] < right[0]:
                newlist.append(left[0])
                del left[0]
            else:
                newlist.append(right[0])
                del right[0]

        newlist.extend(left)
        newlist.extend(right)

        return newlist

print(mergesort([2, 5, 3, 8, 6, 9, 1, 4, 7]))

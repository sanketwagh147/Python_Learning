def binary_search_recursive(listy, target):
    if len(listy) == 0:
        return False
    else:
        midpoint = len(listy) //2

        if listy[midpoint] == target:
            return True,midpoint
        else:
            if listy[midpoint] < target:
                return binary_search_recursive(listy[midpoint +1:], target)
            else:
                return binary_search_recursive(listy[:midpoint], target)


listy = list(range(0, 100))
[x, y]=binary_search_recursive(listy, 18)
print(x)
print(y)

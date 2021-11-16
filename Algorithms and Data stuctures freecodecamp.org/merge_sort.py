def merge_sort(listy):
    """
    :param list:
    :return: sorts a list in ascending order

    Divide: Find the midpoint of the list and divide it into sublist
    Conquer: Recursively sor the sublists created in previous step
    """
    if len(listy) <=1:
        return listy

    left_half, right_half = split(listy)
    left = merge_sort(left_half)
    right = merge_sort(right_half)
    return merge(left, right)




def split(listy):
    """Divide the unsorted list at midpoint into sublists
    Returns two sublists - left and right"""
    mid_point = len(listy)//2
    left = listy[:mid_point]
    right = listy[mid_point:]

    return left, right

def merge(left, right):
    """
    This functiion merges tow list and sorts them and returns a new merged list
    :param left: left list
    :param right:right liset
    :return: Returns a new merged and sorted list
    """
    l =[]
    i = 0
    j = 0
    while i < len(left) and j  < len(right):
        if left[i] < right[j]:
            l.append(left[i])
            i += 1
        else:
            l.append(right[j])
            j += 1

    while i < len(left):
        l.append(left[i])
        i += 1

    while j<len(right):
        l.append(right[i])
        j += 1

    return l
a_list = [54, 63, 93, 17, 77 ,31, 44, 55, 20]
l = merge_sort(a_list)
print(l)






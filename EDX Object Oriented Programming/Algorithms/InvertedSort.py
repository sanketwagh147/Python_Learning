#Write a function called inverted_sort. inverted_ should
#take as input a list of integers, and return as output a
#list with the integers sorted from HIGHEST to LOWEST.
#
#You may use any sorting algorithm you want: bubble, merge,
#insertion, selection, a new sort that you learned on your
#own, or even one you created yourself. You may use loops,
#or you may use recursion.
#
#You may not use Python's native list sort or reverse
#methods; you must write your own sort.


#Write your function here!
# def inverted_sort(a_list):
#     ret_list = []
#     counter = len(a_list)
#
#     while counter > 0:
#         counter -=1
#         max1 = a_list.index(max(a_list))
#         ret_list.append(a_list[max1])
#         a_list.pop(max1)
#     return ret_list
def inverted_sort(a_list):
    ret_list = []
    counter = len(a_list)

    while counter > 0:
        counter -= 1
        max1 = a_list.index(max(a_list))
        ret_list.append(a_list[max1])
        a_list.pop(max1)
    return ret_list



#The code below will test your function. Feel free to
#modify it. As written originally, it will print the list:
# [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
print(inverted_sort([5, 4, 10, 1, 7, 2, 3, 6, 8, 9]))



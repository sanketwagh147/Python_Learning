def linear_search(listy, n, x):
    for i in range( 0, n):
        if x == listy[i]:
            print("Found")
        else:
            print("Not Found")
# Python3 code to linearly search x in arr[].
# If x is present then return its location,
# otherwise return -1
listy = [2, 3, 4, 10, 40]
n = len(listy)

x = 40
result = linear_search(listy, n, x)

# Geeks for Geeks code
# def search(arr, n, x):
#
# 	for i in range(0, n):
# 		if (arr[i] == x):
# 			return i
# 	return -1
#
#
# # Driver Code
# arr = [2, 3, 4, 10, 40]
# x = 56
# n = len(arr)
#
# # Function call
# result = search(arr, n, x)
# if(result == -1):
# 	print("Element is not present in array")
# else:
# 	print("Element is present at index", result)



# Geeks for Geeks
# Python3 Program for recursive binary search.


# Returns index of x in listy if present, else -1
def binarySearch (listy, pointer, list_lenght, x):

	# Check base case
	if list_lenght >= pointer:

		mid = pointer + (list_lenght - pointer) // 2

		# If element is present at the middle itself
		if listy[mid] == x:
			return mid

		# If element is smaller than mid, then it
		# can only be present in left
		elif listy[mid] > x:
			return binarySearch(listy, pointer, mid-1, x)

		# Else the element can only be present
		# in right sublistyay
		else:
			return binarySearch(listy, mid + 1, list_lenght, x)

	else:
		# Element is not present in the list
		return -1

# Driver Code
listy = [ 2, 3, 4, 10, 40 ]
x =4

# Function call
result = binarySearch(listy, 0, len(listy)-1, x)
print(result)

if result != -1:
	print ("Element is present at index % d" % result)
else:
	print ("Element is not present in listyay")


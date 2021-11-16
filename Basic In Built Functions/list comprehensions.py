# The above will fine if there a even item in the row[2] in every item in test_list

import numpy as np
test_list = [[1,2,3], [2, 5, 6], [3, 8, 14]]
new_list = [row[0]+1 for row in test_list]
# print(new_list)


#advanced link comprehensions
even_list = [row[2] for row in test_list if row[2] % 2 ==0]
print(even_list)

# use to make array and selecet first two numbers and make a list of tuples
x = np.zeros((5,5))
print("Original array:")
print(x)
print("Row values ranging from 0 to 4.")
x += np.arange(5)
print(x)
dubu_list = [(i[0],i[1]) for i in x]

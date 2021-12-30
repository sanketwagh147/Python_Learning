# Usage of else after for


for i in range(2, 10):
    print(i)
    if i == 1:
        break
# This block will only execute if break in above for loop is not executed
else:
    print("loop exitted successfully")

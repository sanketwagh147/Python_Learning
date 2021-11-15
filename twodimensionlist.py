# Add each item with some value

M = [[1,2,3], [4,5,6], [7,8,9] ]
res = [col + 10 for row in M for col in row]
print(res)

# Using If else
for row in M:
    for item in row:
        print(item + 10)
i = 0
j = 10
while i < j:
    print(i)
    print(j)
    i = i + 1
    j = j - 1
    print('looope')

# if loop encounters break then it skips else block
x = 7

while x > 3:  # if this expression is true run the loop else move ahead
    print(f"{x} is less than 3")
    if x == 3:
        break
    
    x -= 1
else:
    print("Only print if while does not exit via break")
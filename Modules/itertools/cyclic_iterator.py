import itertools

count = 0


for i in itertools.cycle("AB"):
    print(i)
    count += 1
    if count>5: break
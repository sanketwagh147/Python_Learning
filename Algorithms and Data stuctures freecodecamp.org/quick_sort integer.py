import random

numbers = [ 1, 4345, 123 ,124 ,23]
def is_sorted(values):
    for index in range(len(values)-1):
        if values[index] > values [index + 1]:
            return False
        return True

def bogo_sort(values):
    attempts = 0
    while not is_sorted(values):
        print(attempts)
        random.shuffle(values)
        attempts += 1
    return values

print(bogo_sort(numbers))


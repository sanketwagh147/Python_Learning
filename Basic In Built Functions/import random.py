import random
#To print a random value float between 0 and 1
rand = random.random()
print(rand)

#  To print a random number from a list specified
a = random.choice(list(range(1, 10)))
print(a)

# To print a random integer between a range 1 and 100
b = random.randint(1, 100)
print(b)

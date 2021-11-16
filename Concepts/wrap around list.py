"""This help to wrap around a list
suppose we have iterate to list and print the item but this task should be repeated
by a_number then to wrap the list following code is useful"""

a_number = 7
a_list = ["a", "b", "c", "d"]

for i in range(0, a_number):
    print(a_list[i % len(a_list)])

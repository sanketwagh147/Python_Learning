#Imagine you are on a treasure hunt. You start the
#treasure hunt at position 0, 0. The first coordinate
#represents your steps in the East-West direction, and
#the second coordinate represents your steps in the
#North-South direction. North and East are considered
#'positive' while South and West are considered
#'negative'.
#
#You are then given a list of steps, such as North 5:
#if from the starting spot you go North 5 steps, your
#new location is 0, 5. If your next step is West 3,
#then your new location is -3, 5.
#
#Write a function called treasure_hunt. treasure_hunt
#should take as input a list of tuples, representing the
#steps to complete. In each tuple, the first item will
#be a string ("North", "South", "East", or "West"), and
#the second item will be an integer (the number of
#spaces to move).
#
#The function should return the final coordinate as a
#tuple. For example, if you were given the following list
#of tuples:
#
# [("North", 5), ("West", 3), ("South", 7), ("East", 5),
#  ("South", 2), ("East", 1), ("West", 5), ("North", 4)]
#
#...then the answer would be -2, 0: for the East-West
#direction, -3 + 5 + 1 + -5 = -2, and for the North-South
#direction, 5 + -7 + -2 + 4 = 0.


#Write your function here!
def treasure_hunt(list_of_tuples):
    lat = ["East", "West"]
    lon = ["North", "South"]
    ret_list = []
    a=0
    b=0
    for step in list_of_tuples:
        if step[0] in lat:
            if step[0] == "East":
                a += step[1]
            else:
                a -= step[1]

        if step[0] in lon:
            if step[0] == "North":
                b += step[1]
            else:
                b -= step[1]
    return (a, b)



#Below are some lines of code that will test your function.
#You can change the value of the variable(s) to test your
#function with different inputs.
#
#If your function works correctly, this will originally
#print:
#(-2, 0)
print(treasure_hunt([("North", 5), ("West", 3), ("South", 7), ("East", 5), ("South", 2), ("East", 1), ("West", 5), ("North", 4)]))


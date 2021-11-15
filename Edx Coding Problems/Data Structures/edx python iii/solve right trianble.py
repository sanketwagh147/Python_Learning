#Write a function called solve_right_triangle. The function
#solve_right_triangle should have three parameters: opposite,
#adjacent, and use_degrees. opposite and adjacent will be
#floats, and use_degrees will be a boolean. use_degrees
#should be a keyword parameter, and it should have a
#default value of False.
#
#The function should return a tuple containing the
#hypotenuse and angle of the right triangle (in that order).
#If use_degrees is False, the angle should be in radians.
#If use_degrees is True, the angle should be in degrees.
#
#Remember, the formula for the hypotenuse of a right
#triangle is the square root of the sum of the squared side
#lengths. You can find arctan using math.atan(), passing in
#the quotient of the opposite and adjacent as the argument.
#By default, math.atan() returns the angle in radians; you
#can pass that angle as an argument into the math.degrees()
#method to convert it to degrees; for example:
#
# angle_in_degrees = math.degrees(angle_in_radians)

import math


#Write your function here!
def solve_right_triangle(opposite, adjacent, use_degrees = False):
    hypotenuse = math.sqrt(opposite*opposite + adjacent*adjacent)
    # print(hypotenuse)
    angle_radians=math.atan(opposite/adjacent)
    # print(angle_radians)
    angle_degree=math.degrees(angle_radians)
    # print(angle_degree)
    if use_degrees == True:
        return (hypotenuse, angle_degree)
    else:
        return (hypotenuse, angle_radians)

#Below are some lines of code that will test your function.
#You can change the value of the variable(s) to test your
#function with different inputs.
#
#If your function works correctly, this will originally
#print:
#(5.0, 0.6435011087932844)
#(5.0, 36.86989764584402)
print(solve_right_triangle(3.0, 4.0))
print(solve_right_triangle(3.0, 4.0, use_degrees = True))


#  EDx sample Answers

import math

#First, because we want to assume use_degrees is False but
#let it be overriden, it needs to be a keyword parameter in
#our parameter list:

def solve_right_triangle(opposite, adjacent, use_degrees = False):

    #Next, let's calculate the hypotenuse. The hypotenuse
    #has the same formula regardless of whether we're using
    #degrees or radians: the square root of the sides squared.
    #The easiest way to do square root is to raise the value
    #to the 0.5 power, so we can do this in a relatively short
    #line:

    hypotenuse = (opposite ** 2 + adjacent ** 2) ** 0.5

    #We could also use math.sqrt -- for example:
    #hypotenuse = math.sqrt(opposite ** 2 + adjacent ** 2)
    #
    #Next, we want to calculate the angle. As mentined in the
    #directions, the angle is the inverse tangent, or arctan,
    #of the quotient of the opposite and adjacent. arctan is
    #available in math.atan:

    angle = math.atan(opposite / adjacent)

    #This gives the angle in radians. If we want it in degrees,
    #we need to convert it to degrees:

    if use_degrees == True:
        angle = math.degrees(angle)

    #Now, we can return the tuple with the hypotenuse and angle:

    return (hypotenuse, angle)


print(solve_right_triangle(3.0, 4.0))
print(solve_right_triangle(3.0, 4.0, use_degrees = True))



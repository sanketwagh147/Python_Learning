#A significant part of introductory physics is calculating
#the net force on an object based on several different
#magnitudes and directions. If you're unfamiliar with how
#this works, we recommend checking out this WikiHow article:
#https://www.wikihow.com/Find-Net-Force
#
#Each force acting on the object is defined by its angle and
#magnitude. The process for calculating net force is:
#
# - For each force, break the force into its horizontal and
#   vertical components. The horizontal component can be
#   calculated as magnitude * cos(angle), and the vertical
#   component can be calculated as magnitude * sin(angle).
# - Sum all the horizontal components to find the total
#   horizontal force, and sum the vertical components to find
#   the total vertical force.
# - Use the Pythagorean theorem to calculate the total
#   magnitude: sqrt(total_horizontal ^ 2 + total_vertical ^ 2)
# - Use inverse tangent to calculate the angle:
#   atan2(total_vertical, total_horizontal)
#
#Write a function called find_net_force. find_net_force should
#take one parameter as input: a list of 2-tuples. Each 2-tuple
#in the list is a (magnitude, angle) pair. angle will be in
#degrees between -180 and 180.
#
#Return a 2-tuple containing the final magnitude and angle of
#all the forces. angle should again be in degrees. You should
#round both magnitude and angle to one decimal place, which
#you can do using round(magnitude, 1) and round(angle, 1).
#
#To do this, you'll need to use a few functions from the math
#module in Python. The line below will import these:

from math import sin, cos, tan, asin, acos, atan2, radians, degrees, sqrt

#sin, cos, and tan are the trigonometric functions for sine,
#cosine, and tangent. Each takes one argument, an angle in
#radians, and returns its sine, cosine, or tangent.
#
#asin, acos, and atan2 are their inverse functions. Each
#takes two arguments, a vertical component and a horizontal
#component (in that order), and returns the corresponding
#angle in radians.
#
#Note that sin, cos, and tan all assume the angle is in
#radians, and asin, acos, and atan2 will all return an
#angle in radians. So, you'll need to convert your angles to
#radians before or after using these functions, using things
#like this: angle_in_radians = radians(angle)
#           angle_in_degrees = degrees(angle_in_radians)

#sqrt will find the square root of a number, e.g. sqrt(4) = 2.
#Note that you should only need sin, cos, atan2, degrees,
#radians, and sqrt: we've imported the others just in case you
#want to use them.


#Add your function here!
def find_net_force(a_list):
    total_vertical_force = 0
    total_horizontal_force = 0
    for each in range(0, len(a_list)):
        individual_tuple=a_list[each]
        # print(individual_tuple, end=" :this is individual tuple\n")
        magnitude = individual_tuple[0]
        # print(magnitude, end=" : This is magnitude of individual tuple\n")
        angle = radians(individual_tuple[1])
        # print(angle, end=" : This is angle of individual tuple\n")
        horizontal_component = magnitude * cos(angle)
        # print(horizontal_component)
        vertical_component = magnitude * sin(angle)
        # print(vertical_component)
        total_horizontal_force+=horizontal_component
        total_vertical_force+=vertical_component
    # print(total_vertical_force)
    # print(total_horizontal_force)
    total_magnitude = sqrt((total_horizontal_force)**2+(total_vertical_force)**2)
    # print(round(total_magnitude,2))
    final_angle =  atan2(total_vertical_force, total_horizontal_force)
    final_angle_in_degrees = degrees(final_angle)
    # print(round(final_angle_in_degrees, 2))
    return (round(total_magnitude,1), round(final_angle_in_degrees, 1))

#Below are some lines of code that will test your function.
#You can change the value of the variable(s) to test your
#function with different inputs.
#
#If your function works correctly, this will originally
#print: (87.0, 54.4)

forces = [(10, 90), (10, -90), (100, 45), (20, 180)]
print(find_net_force(forces))


# EDX sample

from math import sin, cos, tan, asin, acos, atan2, radians, degrees, sqrt

#First, we define the function:
def find_net_force(forces):

    #We know from the directions that our goal is to find the
    #total horizontal and total vertical forces. So, let's
    #create variables to hold those values so we can add to
    #them as we go along:
    total_horizontal = 0
    total_vertical = 0

    #Now, let's iterate through each force in the forces:
    for force in forces:

        #To make our code easier to read, let's pull the
        #magnitude and angle out from the tuple:
        magnitude, angle = force

        #The directions told us we need to convert our
        #angles to radians to use Python's trignometric
        #functions:
        angle = radians(angle)

        #Now, the horizontal component is the magnitude
        #times the cosine of the angle:
        horizontal = magnitude * cos(angle)

        #And the vertical component is the magnitude times
        #the sine of the angle:
        vertical = magnitude * sin(angle)

        #Now that we've calculated the horizontal and
        #vertical components, let's add those to our
        #running tallies:
        total_horizontal += horizontal
        total_vertical += vertical

    #The net magnitude is the hypotenuse of the triangle
    #with these two components as their legs. So, we can
    #calculate the net magnitude using the Pythagorean
    #theorem:
    net_magnitude = sqrt(total_horizontal**2 + total_vertical**2)

    #Then as instructed, we round it to one decimal point:
    net_magnitude = round(net_magnitude, 1)

    #Next, we need to calculate the angle. As directed, we
    #do this with the atan2 function from Python's math
    #library, which takes the vertical and horizontal
    #components as arguments:
    net_angle = atan2(total_vertical, total_horizontal)

    #Then, we convert this back to degrees:
    net_angle = degrees(net_angle)

    #And round it to one decimal point as instructed:
    net_angle = round(net_angle, 1)

    #Last, we return the tuple of the madnitude and angle:
    return (net_magnitude, net_angle)

forces = [(10, 90), (10, -90), (100, 45), (20, 180)]
print(find_net_force(forces))





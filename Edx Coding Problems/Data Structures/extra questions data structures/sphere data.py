#Write a function called sphere_data. volume_and_area will
#take in a dictionary. This dictionary is guaranteed to
#have exactly one key: "radius", whose value is an integer
#representing the radius of a sphere.
#
#Modify this dictionary to add two keys: "volume" and "area".
#The values associated with these keys should be the volume
#and surface area of the sphere.
#
#The formula for volume is:
#  (4/3) * pi * radius ^ 3
#
#The formula for surface area is:
#  4 * pi * radius ^ 2
#
#Both volume and surface area should be rounded to two
#decimal places. You can do this with round(val, 2).
#
#The line below will let you use pi as a variable in your
#code, with a value of pi to the 15th decimal place.
from math import pi

#Add your code here!
from math import pi as poo
sphere = {}
def sphere_data(a_dict):
    radius = a_dict.values()
    # print(a_dict["radius"])

    sphere["radius"] = a_dict["radius"]
    sphere["volume"] = round((4/3) * poo * a_dict["radius"] ** 3, 2)
    sphere["area"] =round(4 * poo * a_dict["radius"] ** 2, 2)
    print(sphere)
    return sphere

#Below are some lines of code that will test your function.
#You can change the value of the variable(s) to test your
#function with different inputs.
#
#If your function works correctly, this will originally
#print 4.19 and 12.57, each on a different line.
sphere = {"radius": 7}
sphere = {"radius": 8}
sphere = sphere_data(sphere)
print(sphere["volume"])
print(sphere["area"])
print(u"\u03c0")





class Person:
    def __init__(self, name, eyecolor, age):
        self.name = name
        self.eyecolor = eyecolor
        self.age = age

class Name:
    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname

myPerson1 = Person(Name("David", "Joyner"), "brown", 30)
"""
# case 1: pointing to mutable type
In the below line my person2 first parameter name points to mutable object thus when we modify
it both instances are modified simultaneously
print(myPerson1.name.firstname) >> 
print(myPerson2.name.firstname) >>
both above statement will have the same value
"""

myPerson2 = Person(myPerson1.name, myPerson1.eyecolor, myPerson1.age)
"""
# case 2: pointing to immutable type
In the below line my person2 first parameter name points to immutable object thus when we modify
it both instances are modified not modified simultaneously
print(myPerson1.name.firstname) >> 
print(myPerson2.name.firstname) >>
both above statement will not have the same value
"""

myPerson2 = Person(Name(myPerson1.name.firstname, myPerson1.name.lastname),
                   myPerson1.eyecolor, myPerson1.age)
myPerson2.eyecolor = "blue"
print(myPerson1.eyecolor)
print(myPerson2.eyecolor)
myPerson2.name.firstname = "Vrushali"
print(myPerson1.name.firstname)
print(myPerson2.name.firstname)



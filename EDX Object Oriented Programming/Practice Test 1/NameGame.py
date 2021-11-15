#Create a class called Name. Name should have two attributes
#(instance variables): first_name and last_name. Make sure
#the variable names match those words. Both will be strings.
#
#Name should have a constructor with two required parameters,
#one for each of those attributes (first_name and last_name,
#in that order).
#
#Name should also have two methods. The first should be
#called find_printed_name, and should return the first and
#last name with a space in between, e.g. "David Joyner". The
#second method should be called find_sortable_name, and
#should return the last name, then a comma and space, and
#then only the first initial, e.g. "Joyner, D".
#
#Neither sortable_name nor printed_name should be attributes:
#both should be created and returned when those methods are
#called. Neither method will have any parameters besides self.


#Write your class here!
class Name:
    first_name = str
    last_name = str

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def find_printed_name(self):
        return self.first_name + " " + self.last_name

    def find_sortable_name(self):
        return self.last_name + ", " + self.first_name[0]


#Below are some lines of code that will test your function.
#You can change the value of the variable(s) to test your
#function with different inputs.
#
#If your function works correctly, this will originally
#print
#David
#Joyner
#David Joyner
#Joyner, D
test_name = Name("David", "Joyner")
print(test_name.first_name)
print(test_name.last_name)
print(test_name.find_printed_name())
print(test_name.find_sortable_name())







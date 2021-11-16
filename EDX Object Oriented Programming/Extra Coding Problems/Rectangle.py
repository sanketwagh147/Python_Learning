#Create a class called Rectangle. Rectangle should
#have two attributes (instance variables): length and
#width. Make sure the variable names match those words.
#Both will be floats.
#
#Rectangle should have a constructor with two required
#parameters, one for each of those attributes (length and
#width, in that order).
#
#Rectangle should also have a method called
#find_perimeter. find_perimeter should calculate the
#perimeter of the rectangle based on the current values for
#length and width.
#
#perimeter should NOT be an attribute of the class; instead,
#perimeter should be calculated and returned live when the
#ethod find_perimeter is called.
#
#The find_perimeter method should have NO parameters
#besides self. Instead, it should calculate the perimeter
#based on the current values for the opposite and adjacent
#attributes.
#
#Hint: The formula for perimeter is 2 * length + 2 * width.


#Write your class here!
class Rectangle:
    length = float
    width = float

    def __init__(self,length, width):
        self.length = length
        self.width = width

    def find_perimeter(self):
        return self.length*2 + self.width*2


#The code below will test your function. If it works, it
#should print 3.0, 4.0, and 14.0 in that order.
test_rectangle = Rectangle(3.0, 4.0)
print(test_rectangle.length)
print(test_rectangle.width)
print(test_rectangle.find_perimeter())



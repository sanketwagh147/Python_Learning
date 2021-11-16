#10th Street Trade School is a small university. It
#currently offers 12 majors: Accounting, Architecture,
#Astronomy, Business, Economics, History, Law, Medicine,
#Neuroscience, Physics, Psychology, and Zoology.
#
#10th Street's class-numbering structure is the same as
#Georgia Tech's: all classes have 4-digit numbers;
#undergraduate classes have numbers in the 1000s, 2000s,
#3000s, or 4000s, while graduate classes have numbers in
#the 6000s, 7000s, or 8000s.
#
#For three majors, 10th Street offers only undergraduate
#classes: Business, Architecture, and History. For three,
#it offers only graduate classes: Law, Medicine, and
#Neuroscience. For the other six, it offers both
#undergraduate and graduate classes.
#
#However, four majors are not offered during the summer:
#Business, Law, Architecture, and Accounting are only
#offered in Spring and Fall semesters.
#
#Write a function called check_class. check_class should
#require two positional arguments: a string for major
#name ("Astronomy", "Physics", etc.) and an integer for
#class number (1001, 6750, etc.). It should also have
#one keyword parameter: is_summer. is_summer should be
#False by default.
#
#check_class should return True if the class is valid,
#or False if it is not. A class is valid if (a) its
#major is one of the 12 majors listed above, (b) its
#class number is appropriate for the major (6000
#through 8999 for graduate-only majors, 1000 through
#4999 for undergraduate-only majors, or either for
#other majors, but nothing outside that range), and
#(c) the class is offered during the given semester
#(e.g. it's always offered, or it's not a summer
#semester).


#Write your function here!


#Below are some lines of code that will test your function.
#You can change the value of the variable(s) to test your
#function with different inputs.
#
#If your function works correctly, this will originally
#print: True, False, False, False, False, False
print(check_class("Accounting", 1001))
print(check_class("Accounting", 1001, is_summer = True))
print(check_class("Law", 2001))
print(check_class("History", 6500))
print(check_class("Basket-Weaving", 3500))
print(check_class("Astronomy", 5500))



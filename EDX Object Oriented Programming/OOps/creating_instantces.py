#Define the class Person
class Person:
    #Create a new instance of Person
    def __init__(self):
        #Person's default values
        self.firstname = "[no first name]"
        self.lastname = "[no last name]"
        self.eyecolor = "[no eye color]"
        self.age = -1
        kanda= "5"
        print(kanda)

#Create a new Person and assign it to myPerson
myPerson = Person()
sanket = Person()
sanket.age = 29
sanket.firstname = "sanket"
sanket.lastname = "wagh"
sanket.eyecolor = "black"
#Print myPerson's values
print(myPerson.firstname)
print(myPerson.lastname)
print(myPerson.eyecolor)
print(myPerson.age)
sanket.firstname = sanket.firstname.upper()


print(sanket.firstname, "The", sanket.lastname)

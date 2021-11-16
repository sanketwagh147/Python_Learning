#Copy your Burrito class from the last exercise. Now,
#write a getter and a setter method for each attribute.
#Each setter should accept a value as an argument. If the
#value is a valid value, it should set the corresponding
#attribute to the given value. Otherwise, it should set the
#attribute to False.
#
#Edit the constructor to use these new setters and getters.
#In other words, if we were to call:
#
# new_burrito = Burrito("spaghetti", True, True, False)
#
#new_burrito.meat would be False because "spaghetti" is not
#one of the valid options. Note that you should NOT try to
#check if the new value is valid in both the constructor and
#the setter: instead, just call the setter from the
#constructor using something like self.set_meat(meat).
#
#Valid values for each setter are as follows:
#
# - set_meat: "chicken", "pork", "steak", "tofu", False
# - set_to_go: True, False
# - set_rice: "brown", "white", False
# - set_beans: "black", "pinto", False
# - set_extra_meat: True, False
# - set_guacamole: True, False
# - set_cheese: True, False
# - set_pico: True, False
# - set_corn: True, False
#
#Make sure you name each setter with the format:
#"set_some_attribute" and "get_some_attribute"
#
#For example, the getter for meat would be get_meat. The
#getter for to_go would be get_to_go.
#
#Hint: Your code is going to end up *very* long. This
#will be the longest program you've written so far, but
#it isn't the most complex. Complexity and length are
#often very different!
#
#Hint 2: Checking for valid values will be much easier
#if you make a list of valid values for each attribute
#and check the new value against that.


#Write your code here!
class Burrito:
    def __init__(self, meat, to_go, rice, beans, extra_meat=False, guacamole=False, cheese=False, pico=False, corn=False):
        self.meat = self.set_meat(meat)
        self.to_go = self.set_to_go(to_go)
        self.rice = self.set_rice(rice)
        self.beans = self.set_beans(beans)
        self.guacamole = self.set_guacamole(guacamole)
        self.extra_meat = self.set_extra_meat(extra_meat)
        self.cheese = self.set_cheese(cheese)
        self.pico = self.set_pico(pico)
        self.corn = self.set_corn(corn)

    def get_meat(self):
        # print("3")
        print(self.meat)
        return self.meat

    def get_to_go(self):
        return self.to_go

    def get_corn(self):
        return self.corn

    def get_rice(self):
        return self.rice

    def get_extra_meat(self):
        return self.extra_meat

    def get_pico(self):
        return self.pico

    def get_cheese(self):
        return self.cheese

    def get_beans(self):
        return self.beans

    def get_guacamole(self):
        return self.guacamole

    def set_meat(self, meat):
        meat_list = ["chicken", "pork", "steak", "tofu", False]
        if meat in meat_list:
            # print(meat)
            self.meat = meat
            # print("1")
            return self.meat
        else:
            self.meat = False
            # print("2")
            return False

    def set_to_go(self, to_go):
        if isinstance(to_go, bool):
            self.to_go = to_go
            return self.to_go
        else:
            self.to_go = False
            return False

    def set_rice(self, rice):
        rice_list = ["brown", "white", False]
        if rice in rice_list:
            self.rice = rice
            return self.rice
        else:
            self.rice = False
            return False

    def set_beans(self, beans):
        beans_list = ["black", "pinto", False]
        if beans in beans_list:
            self.beans = beans
            return self.beans
        else:
            self.beans = False
            return False

    def set_extra_meat(self, extra_meat):
        if isinstance(extra_meat, bool):
            self.extra_meat = extra_meat
            return self.extra_meat
        else:
            self.extra_meat = False
            return False

    def set_guacamole(self, guacamole):
        if isinstance(guacamole, bool):
            self.guacamole = guacamole
            return self.guacamole
        else:
            self.guacamole = False
            return False

    def set_cheese(self, cheese):
        if isinstance(cheese, bool):
            self.cheese = cheese
            return self.cheese
        else:
            self.cheese = False
            return False

    def set_pico(self, pico):
        if isinstance(pico, bool):
            self.pico = pico
            return self.pico
        else:
            self.pico = False
            return False

    def set_corn(self, corn):
        if isinstance(corn, bool):
            self.corn = corn
            return self.corn

        else:
            self.corn = False
            return False
#Feel free to add code below to test out the class that
#you've written. It won't be used for grading.


# We called burrito_1.set_meat("pineapple"),
# then called burrito_1.get_meat(). We expected burrito_1.get_meat() to return the bool False,
# but instead it returns the str "pork".
burrito_1 = Burrito("pineaple", True, True, True)
burrito_1.set_meat("chicken")


# EDx Solution
# Our initial class definition and constructor header are
# the same as before:
class Burrito:
    def __init__(self, meat, to_go, rice, beans, extra_meat=False, guacamole=False, cheese=False, pico=False, corn=False):

        #Note, though, that inside the constructor, we're
        #now calling self.set_meat and the other setters.
        #This way, we only have to have our data validation
        #in one place, inside the setters. When we create a
        #new instance of Burrito, we automatically call the
        #methods that check whether the input is valid.
        self.set_meat(meat)
        self.set_to_go(to_go)
        self.set_rice(rice)
        self.set_beans(beans)
        self.set_extra_meat(extra_meat)
        self.set_guacamole(guacamole)
        self.set_cheese(cheese)
        self.set_pico(pico)
        self.set_corn(corn)

    #All our getters just return the corresponding values:
    def get_meat(self):
        return self.meat

    def get_to_go(self):
        return self.to_go

    def get_rice(self):
        return self.rice

    def get_beans(self):
        return self.beans

    def get_extra_meat(self):
        return self.extra_meat

    def get_guacamole(self):
        return self.guacamole

    def get_cheese(self):
        return self.cheese

    def get_pico(self):
        return self.pico

    def get_corn(self):
        return self.corn

    #Each setter first compares the new value to a list of
    #acceptable values. If the new value is in that list, it
    #sets its value for that attribute equal to the new value.
    #If not, it sets its value for that attribute equal to
    #False:
    def set_meat(self, new_value):
        if new_value in ["chicken", "steak", "pork", "tofu", False]:
            self.meat = new_value
        else:
            self.meat = False

    def set_to_go(self, new_value):
        if new_value in [True, False]:
            self.to_go = new_value
        else:
            self.to_go = False

    def set_rice(self, new_value):
        if new_value in ["white", "brown", False]:
            self.rice = new_value
        else:
            self.rice = False

    def set_beans(self, new_value):
        if new_value in ["black", "pinto", False]:
            self.beans = new_value
        else:
            self.beans = False

    def set_extra_meat(self, new_value):
        if new_value in [True, False]:
            self.extra_meat = new_value
        else:
            self.extra_meat = False

    def set_guacamole(self, new_value):
        if new_value in [True, False]:
            self.guacamole = new_value
        else:
            self.guacamole = False

    def set_cheese(self, new_value):
        if new_value in [True, False]:
            self.cheese = new_value
        else:
            self.cheese = False

    def set_pico(self, new_value):
        if new_value in [True, False]:
            self.pico = new_value
        else:
            self.pico = False

    def set_corn(self, new_value):
        if new_value in [True, False]:
            self.corn = new_value
        else:
            self.corn = False



    def get_cost(self):
        base_cost = 5.00
        if self.meat in ["chicken", "pork", "tofu"]:
            base_cost += 1.0

        elif self.meat == "steak":
            base_cost += 1.5

        else:
            self.meat = False

        if self.extra_meat == True:
            base_cost += 1.0

        if self.guacamole==True:
            base_cost += 0.75

        self.cost = base_cost

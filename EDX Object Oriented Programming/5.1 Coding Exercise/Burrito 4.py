#Copy your Burrito class from the last exercise. Below,
#We've given you three additional classes named "Meat",
#"Rice" and "Beans." We've gone ahead and built getters
#and setters in these classes to check if the incoming
#values are valid, so you'll be able to remove those
#from your original code.
class Burrito:
    def __init__(self, meat, to_go, rice, beans, extra_meat=False, guacamole=False, cheese=False, pico=False, corn=False):
        self.meat = Meat(meat)
        self.to_go = self.set_to_go(to_go)
        self.rice = Rice(rice)
        self.beans = Beans(beans)
        self.guacamole = self.set_guacamole(guacamole)
        self.extra_meat = self.set_extra_meat(extra_meat)
        self.cheese = self.set_cheese(cheese)
        self.pico = self.set_pico(pico)
        self.corn = self.set_corn(corn)
        self.base_cost = 0

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

    # def set_rice(self, rice):
    #     rice_list = ["brown", "white", False]
    #     if rice in rice_list:
    #         self.rice = rice
    #         return self.rice
    #     else:
    #         self.rice = False
    #         return False

    # def set_beans(self, beans):
    #     beans_list = ["black", "pinto", False]
    #     if beans in beans_list:
    #         self.beans = beans
    #         return self.beans
    #     else:
    #         self.beans = False
    #         return False

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

    def get_cost(self):
        self.base_cost = 5.00
        # print("1")
        print(self.meat.meat, " self.meat")
        if self.meat.meat in ["chicken", "pork", "tofu"]:
            self.base_cost += 1.0
            print(self.base_cost,"meat included cose added")

        elif self.meat == "steak":
            self.base_cost += 1.5
            # print("2.1")

        else:
            self.base_cost += 0
            # print("2.2")

        print(self.extra_meat)
        if self.extra_meat and self.meat.meat != False:
            self.base_cost += 1.0
            print("3")
        else:
            self.base_cost += 0
            print("2.3")
        print(self.guacamole)
        if self.guacamole:
            self.base_cost += 0.75
            # print("4")
        else:
            self.base_cost += 0
            # print("2.4")
        print(self.base_cost, "base_cost before return")
        # print("147")
        return self.base_cost
#
#First, edit the constructor of your Burrito class.
#Instead of calling setters to set the values of the
#attributes self.meat, self.rice, and self.beans, it
#should instead create new instances of Meat, Rice, and
#Beans. The arguments to these new instances should be
#the same as the arguments you were sending to the
#setters previously (e.g. self.rice = Rice("brown")
#instead of set_rice("brown")).
#
#Second, modify your getters and setters from your
#original code so that they still return the same value
#as before. get_rice(), for example, should still
#return "brown" for brown rice, False for no rice, etc.
#instead of returning the instance of Rice.
#
#Third, make sure that your get_cost function still
#works when you're done changing your code.
#
#Hint: When you're done, creating a new instance of
#Burrito with Burrito("pork", True, "brown", "pinto")
#should still work to create a new Burrito. The only
#thing changing is the internal reasoning of the
#Burrito class.
#
#Hint 2: Notice that the classes Meat, Beans, and Rice
#already contain the code to validate whether input is
#valid. So, your setters in the Burrito class no
#longer need to worry about that -- they can just pass
#their input to the set_value() methods for those
#classes.
#
#Hint 3: This exercise requires very little actual
#coding: you'll only write nine lines of new code, and
#those nine lines all replace existing lines of code
#in the constructor, getters, and setters of Burrito.
#
#You should not need to modify the code below.

class Meat:
    def __init__(self, value=False):
        self.set_meat(value)

    def get_value(self):
        return self.meat
#Nevermind the issue was in the setters methods. For example, in the set_rice method,
    # it should be self.rice.set_value(rice) instead of set_value(rice).
    def set_meat(self, meat):
        meat_list = ["chicken", "pork", "steak", "tofu", False]
        if meat in meat_list:
            # print(meat)
            self.meat. = meat
            # print("1")
            return self.meat
        else:
            self.meat = False
            # print("2")
            return False

class Rice:
    def __init__(self, value=False):
        self.set_value(value)

    def get_value(self):
        return self.value

    def set_value(self, value):
        if value in ["brown", "white"]:
            self.value = value
        else:
            self.value = False

class Beans:
    def __init__(self, value=False):
        self.set_value(value)

    def get_value(self):
        return self.value

    def set_value(self, value):
        if value in ["black", "pinto"]:
            self.value = value
        else:
            self.value = False



#Add and modify your code here!



#Below are some lines of code that will test your class.
#You can change the value of the variable(s) to test your
#class with different inputs. Remember though, the results
#of this code should be the same as the previous problem:
#what should be different is how it works behind the scenes.
#
#If your function works correctly, this will originally
#print: 7.75

# a_burrito = Burrito("pork", False, "white", "black", extra_meat = True, guacamole = True)
# print(a_burrito.get_cost())
# print(a_burrito.meat.meat)
# print(a_burrito.beans.value)
# print(a_burrito.rice.value)
print(">>>>>>>>>>>>>>>>>>>>>>>>>")
# #We expected burrito_1.get_cost() to return 7.75. However, it returned 6.75.
# burrito_1 = Burrito("pork", False, "white", "black", extra_meat = True, guacamole = True)
# print(burrito_1.get_cost(), 7.75)
# #
# # We expected burrito_2.get_cost() to return 6.0. However, it returned 5.0.
# burrito_2 = Burrito("chicken", False, "crony", "pinto", extra_meat = "gaur", guacamole = False, cheese = True, pico = True, corn = True)
# print(burrito_2.get_cost(), 6.0)
# # We called burrito_2.set_extra_meat(False), then we called burrito_2.get_cost() again.
# # We expected burrito_2.get_cost() o return 6.0. However, it returned 5.0.
# burrito_2.set_extra_meat(False)
# print(burrito_2.get_cost(), 6.0)
# #
# # We expected burrito_3.get_cost() to return 5.0. However, it returned 6.0.
# burrito_3 = Burrito("phrasemake", True, "Hetty", "black", extra_meat = True, guacamole = "gaur", cheese = "gaur", pico = True, corn = False)
# print(burrito_3.get_cost(), 5.0)
# # We called burrito_3.set_meat(False), then we called burrito_3.get_cost() again.
# # We expected burrito_3.get_cost() to return 5.0. However, it returned 6.0.
# burrito_3.set_meat(False)
# print(burrito_3.get_cost(), 5.0)
burrito_2 = Burrito(False, False, "brown", False, extra_meat = True, guacamole = False, cheese = False, pico = True, corn = True)
# We expected burrito_2.get_cost() to return 5.0. However, it returned 6.0.
print(burrito_2.get_cost(), 5.0)

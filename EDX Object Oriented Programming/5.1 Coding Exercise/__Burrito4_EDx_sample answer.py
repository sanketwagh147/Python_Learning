#As noted, this problem requires very little new code:
#instead, the challenge is in knowing what to change.
#Below is a correct answer: the changes are marked.
#
#First, this code is unchanged:
class Meat:
    def __init__(self, value=False):
        self.set_value(value)

    def get_value(self):
        return self.value

    def set_value(self, value):
        if value in ["chicken", "pork", "steak", "tofu"]:
            self.value = value
        else:
            self.value = False

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

#Here is our burrito class. Changes are marked with in-line
#comments:
class Burrito:
    def __init__(self, meat, to_go, rice, beans, extra_meat = False, guacamole = False, cheese = False, pico = False, corn = False):
        self.meat = Meat(meat) #Instead of calling the setter,
                               #we create a new instance of Meat.
                               #The reason we don't need to call
                               #the setter is that the constructor
                               #for the Meat class calls its OWN
                               #set_value method, which validates
                               #the input.
        self.set_to_go(to_go)

        self.rice = Rice(rice)    #The same principle applies to Rice
        self.beans = Beans(beans) #and Beans.

        self.set_extra_meat(extra_meat)
        self.set_guacamole(guacamole)
        self.set_cheese(cheese)
        self.set_pico(pico)
        self.set_corn(corn)

    def get_meat(self):
        return self.meat.get_value()  #Now instead of just returning
                                      #self.meat, we need to dig into
                                      #self.meat and return get_value().
                                      #That is because self.meat used to
                                      #be a string, but now it's an
                                      #instance of Meat; but we still want
                                      #this method to do the same thing it
                                      #did before.


    def get_to_go(self):
        return self.to_go

    def get_rice(self):
        return self.rice.get_value()  #The same rationale applies to Rice...

    def get_beans(self):
        return self.beans.get_value() #...and to Beans.

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

    def set_meat(self, new_value):
        self.meat.set_value(new_value)  #set_meat gets easier: the
                                        #validation is inside the
                                        #Meat class, so we just have
                                        #to call self.meat.set_value
                                        #and the Meat class handles
                                        #everything for us.

    def set_to_go(self, new_value):
        if new_value in [True, False]:
            self.to_go = new_value
        else:
            self.to_go = False

    def set_rice(self, new_value):
        self.rice.set_value(new_value)  #The same principle applies to Rice...

    def set_beans(self, new_value):
        self.beans.set_value(new_value) #...and Beans.

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

    #Notice that if we used the getters in the get_cost() method,
    #then we didn't need to change anything here: get_meat() still
    #returns the same thing now as it did before. If we used self.meat,
    #though, this had to change to either self.get_meat() or
    #self.meat.get_value() to make this reasoning work.
    def get_cost(self):
        cost = 5.0
        if self.get_meat() in ["chicken", "pork", "tofu"]:
            cost += 1.0
        if self.get_meat() == "steak":
            cost += 1.5
        if self.get_extra_meat() and self.get_meat():
            cost += 1.0
        if self.get_guacamole():
            cost += 0.75
        return cost


a_burrito = Burrito("pork", False, "white", "black", extra_meat = True, guacamole = True)
print(a_burrito.get_cost())



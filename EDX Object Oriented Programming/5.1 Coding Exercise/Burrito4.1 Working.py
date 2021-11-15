class Meat:
    def __init__(self, value=False):
        self.set_value(value)
        self.meat = self.set_value(value)

    def get_value(self):
        return self.value

    def set_value(self, value):
        if value in ["chicken", "pork", "steak", "tofu"]:
            self.value = value
        else:
            self.value = False
class Rice:
    def init(self, value=False):
        self.set_value(value)
        self.rice = self.set.value(value)

    def get_value(self):
        return self.value

    def set_value(self, value):
        if value in ["brown", "white"]:
            self.value = value
        else:
            self.value = False
class Beans:
    def init(self, value=False):
        self.set_value(value)
        set.beans = self.set.value(value)

    def get_value(self):
        return self.value

    def set_value(self, value):
        if value in ["black", "pinto"]:
            self.value = value
        else:
            self.value = False

class Burrito:
    def __init__(self, meat, to_go, rice, beans, extra_meat = False, guacamole = False, cheese = False, pico = False, corn = False):
        self.meat = Meat(meat)
        self.set_to_go(to_go)
        self.rice = Rice()
        self.beans = Beans()
        self.set_extra_meat(extra_meat)
        self.set_guacamole(guacamole)
        self.set_cheese(cheese)
        self.set_pico(pico)
        self.set_corn(corn)

# Getters
    def get_meat(self):
        return self.meat.get_value()

    def get_to_go(self):
        return self.to_go

    def get_rice(self):
        return self.rice.get_value()

    def get_beans(self):
        return self.beans.get_value()

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

# Setters
    # For example, in the set_rice method, it should be self.rice.set_value(rice)
    #                                           instead of set_value(rice).

    def set_meat(self, meat):
        self.meat.set_value(meat)

    def set_to_go(self, to_go):
        valid_to_go = [True, False]
        if to_go in valid_to_go:
            self.to_go = to_go
        else:
            self.to_go = False

    def set_rice(self, rice):
        self.rice.set_value(rice)

    def set_beans(self, beans):
        set.beans.set_value(beans)

    def set_extra_meat(self, extra_meat):
        valid_extra_meat = [True, False]
        if extra_meat in valid_extra_meat:
            self.extra_meat = extra_meat
        else:
            self.extra_meat = False

    def set_guacamole(self, guacamole):
        valid_guacamole = [True, False]
        if guacamole in valid_guacamole:
            self.guacamole = guacamole
        else:
            self.guacamole = False

    def set_cheese(self, cheese):
        valid_cheese = [True, False]
        if cheese in valid_cheese:
            self.cheese = cheese
        else:
            self.cheese = False

    def set_pico(self, pico):
        valid_pico = [True, False]
        if pico in valid_pico:
            self.pico = pico
        else:
            self.pico = False

    def set_corn(self, corn):
        valid_corn = [True, False]
        if corn in valid_corn:
            self.corn = corn
        else:
            self.corn = False

    # Method to compute cost

    def get_cost(self):
        self.base_cost = 5.00
        print(self.base_cost,":Base Cost")
        print(self.meat.value , " self.meat")
        if self.meat.value in ["chicken", "pork", "tofu"]:
            self.base_cost += 1.0
            print(self.base_cost,"meat included if chicken pork or tofu added")
            print (self.meat, " meat type before steak loop")
        elif self.meat == "steak":
            self.base_cost += 1.5
            print(self.base_cost, ": meat is steak")

        else:
            self.base_cost += 0
            print(self.base_cost, "No meat selected")

        print(self.extra_meat)
        if self.extra_meat and self.meat.value != False:
            self.base_cost += 1.0
            print(self.base_cost, ": Extra meet true price increased by 1")
        else:
            self.base_cost += 0
            print(self.base_cost, ": Extra meet false price same")
        print(self.guacamole)
        if self.guacamole:
            self.base_cost += 0.75
            print(self.base_cost, ": Extra guaca true price increased by 0.75")
        else:
            self.base_cost += 0
            print(self.base_cost, ": Extra guacoa false price same")
        print(self.base_cost, "base_cost before return")
        # print("147")
        return self.base_cost

# burrito_1 = Burrito("pork", False, "white", "black", extra_meat = True, guacamole = True)
#
# print(burrito_1.get_cost()," to return 7.75")
#

# burrito_2 = Burrito("chicken", "village", "brown", False, extra_meat = "village", guacamole = True,
#                     cheese = True, pico = True, corn = False)
# print(burrito_2.get_cost()," to return 6.75")

burrito_2 = Burrito("etymology", False, False, "counterflow", extra_meat = True, guacamole = False, cheese = True, pico = False, corn = False)
print(burrito_2.get_cost()," to return 5")
# burrito_3 = Burrito("tofu", "village", "somersault", "suffuse", extra_meat = True, guacamole = False,
#                     cheese = False, pico = "village", corn = "village")
# print(burrito_3.get_cost(), 'to return 7.0')
# burrito_4 = Burrito("pork", False, "brown", "suffuse", extra_meat = False, guacamole = False,
#                     cheese = False, pico = "village", corn = "village")
#
# burrito_5 = Burrito("tofu", True, "somersault", False, extra_meat = "village", guacamole = False,
#                     cheese = False, pico = False, corn = True)
#
# burrito_6 = Burrito("tofu", "village", False, "gurgle", extra_meat = False, guacamole = True,
#                     cheese = True, pico = False, corn = False)
#


# We expected
#
#
# We called burrito_2.set_extra_meat(True), then we called burrito_2.get_cost() again. We expected burrito_2.get_cost() to return 7.75. However, it returned 6.75.
#
#
# We expected burrito_3.get_cost() to return 7.0. However, it returned 6.0.
#
#
# We called burrito_3.set_meat("Diocletian"), then we called burrito_3.get_cost() again. We expected burrito_3.get_cost() to return 5.0. However, it returned 6.0.
#
#
# We expected burrito_4.get_cost() to return 6.0. However, it returned 5.0.
#
#
# We called burrito_4.set_guacamole(True), then we called burrito_4.get_cost() again. We expected burrito_4.get_cost() to return 6.75. However, it returned 5.75.
#
#
# We expected burrito_5.get_cost() to return 6.0. However, it returned 5.0.


# We called burrito_5.set_extra_meat(False), then we called burrito_5.get_cost() again. We expected burrito_5.get_cost() to return 6.0. However, it returned 5.0.
#
#
# We expected burrito_6.get_cost() to return 6.75. However, it returned 5.75.

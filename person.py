from classtools import AttrDisplay
class Person(AttrDisplay):
    """
    Create and process person records
    """
    total_person = 0
    def __init__(self, name, job=None, pay=0):
        self.name = name
        self.job = job
        self.pay = pay
        # total_person += 1
    def last_name(self):
        return self.name.split()[-1]
    def give_raise(self, percent):
        raise_amount = self.pay * percent
        self.pay = int(self.pay * (1 + percent))
        return raise_amount
    # def __str__(self):
    #     return "[Person:%s, %s%s]" %(self.name,"salary:", self.pay)
    

class Manager(Person):
    def __init__(self,name, pay):
        Person.__init__(self,name,"mgr",pay)
    def give_raise(self,percent, bonus= .10):
        return Person.give_raise(self, percent + bonus)
    def something_else(self):
        return f"{self.name} got a raise of {self.give_raise(.10)}"

class Department:
    def __init__(self, *args):
        self.members = list(args)
    def addMember(self, person):
        self.members.append(person)
    def giveRaises(self, percent):
        for person in self.members:
            person.give_raise(percent)
    def showAll(self):
        for person in self.members:
            print(person)
    
pay = 10000
pay *= 2
if __name__ == '__main__':
    bob = Person('Bob Smith')
    sue = Person('Sue Jones', job='dev', pay=100000)
    print(bob)
    print(sue)
    print(bob.last_name(), sue.last_name())
    sue.give_raise(.10)
    print(sue)
    tom = Manager('Tom Jones', 50000)
    tom.give_raise(.10)
    print(tom.last_name())
    print(tom)

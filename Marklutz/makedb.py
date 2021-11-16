from person import Person, Manager
bob = Person("bobda Builder")
sue = Person("sue soo",job="dev", pay=10000)
tom = Manager("Tom Cruise", 50000)

import shelve
db = shelve.open("persondb")
for obj in (bob, sue, tom):
    db[obj.name] = obj
db.close()

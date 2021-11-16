#This problem uses the same Pet, Owner, and Name classes from
#the previous two problems. In this case, however, we want you
#to modify one of the classes.
#
#Notice that in the previous two problems, we always had to
#create owners and pets in the same order: first create the owner,
#then create the pets, then add the pets to the owner's list
#of pets. If we forgot that last step, then the pet would have
#its owner, but the owner would not have its list of pets.
#We cannot create a pet without an owner (because owner is a
#positional parameter in the constructor __init__), but there
#is nothing forcing us to add the pet to the owner's list of
#pets once created.
#
#Modify the classes below so that when a new instance of Pet
#is created, it is automatically added to its Owner's list of
#pets.
#
#HINT: Remember that the self attribute refers to the instance
#itself. For example, if you wanted your object to say, "add me
#to this_list", you would write the_list.append(self).
#
#HINT 2: If you're stuck, look back at how we added pets to
#owners in test code on the previous problems.


#Modify one or more of the classes below:
class Name:
    def __init__(self, first, last):
        self.first = first
        self.last = last

class Pet:
    def __init__(self, name, owner):
        self.name = name
        self.owner = owner
    def petlist(self):
        pet_list = []
        pet_list.append(self)
        print(pet_list)
        return pet_list
    # def add_pet(self,name, owner):
    #     owner.pets.append(name)

# owner_1.pets.append(pet_1)
# owner_1.pets.append(pet_2)
# owner_2.pets.append(pet_3)

class Owner:
    def __init__(self, name):
        self.name = name
        self.pets = Pet.petlist(self)
#Below are some lines of code that will test your edits.
#Specifically, they will print the number of pets in
#each owner's list of pets. Note that you should note
#add to the code below; the correct output should come
#solely from your changes to the code above.
#
#If your code works correctly, this will originally print:
#2
#1
owner_1 = Owner(Name("David", "Joyner"))
owner_2 = Owner(Name("Audrey", "Hepburn"))

pet_1 = Pet(Name("Boggle", "Joyner"), owner_1)
pet_2 = Pet(Name("Artemis", "Joyner"), owner_1)
pet_3 = Pet(Name("Pippin", "Hepburn"), owner_2)

print(len(owner_1.pets))
print(len(owner_2.pets))


## Edx Solution

#To accomplish this, we need to modify the Pet class to
#reflect the reasoning, "once I've been created, add me
#to my owner's list of Pets." So, we're modifying the Pet
#class:

class Name:
    def __init__(self, first, last):
        self.first = first
        self.last = last

class Pet:
    def __init__(self, name, owner):
        self.name = name
        self.owner = owner

        #At this point in this class, the new instance of
        #Pet knows who its owner is (owner). So, it
        #says, "Add me to my owner's list of pets." The
        #owner's list of pets is owner.pets, and it's a list,
        #so we use the append method:
        owner.pets.append(self)

        #Note that self.owner.pets.append(self) would work,
        #too. self.owner points to the same instance as owner.

class Owner:
    def __init__(self, name):
        self.name = name
        self.pets = []

#Below are some lines of code that will test your edits.
#Specifically, they will print the number of pets in
#each owner's list of pets. Note that you should note
#add to the code below; the correct output should come
#solely from your changes to the code above.
#
#If your code works correctly, this will originally print:
#2
#1
owner_1 = Owner(Name("David", "Joyner"))
owner_2 = Owner(Name("Audrey", "Hepburn"))

pet_1 = Pet(Name("Boggle", "Joyner"), owner_1)
pet_2 = Pet(Name("Artemis", "Joyner"), owner_1)
pet_3 = Pet(Name("Pippin", "Hepburn"), owner_2)

print(len(owner_1.pets))
print(len(owner_2.pets))

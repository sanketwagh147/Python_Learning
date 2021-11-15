#Imagine you're writing a program to check whether sufficient
#inventory exists to fill an incoming order at a store. Your
#current inventory comes in the form of a list of instances of
#an InventoryItem class.
#
#You don't have access to the code for the InventoryItem class.
#However, you know that it has at least two attributes:
#name (a string) and quantity (an integer). The name is the
#product's name, and the quantity is the current number of that
#item that are in stock.
#
#Write a function called sufficient_inventory.
#sufficient_inventory should take three parameters: a list of
#instances of InventoryItem representing the current inventory,
#an item name (a string), and a desired quantity (an integer).
#
#The function should return True if two conditions are met:
#
# (a) There exists an instance of InventoryItem in the list
#     whose name matches the the item name parameter.
# (b) The quantity associated with that instance is larger than
#     the desired quantity.
#
#For example, imagine we called:
#
# sufficient_inventory(my_items, "hat", 3)
#
#This would return True if one of the elements in my_items had
#a name attribute "hat" and a quantity attribute greater than
#or equal to 3. It would return False if either no item in
#my_items had the name "hat", or item with the name "hat"
#has a quantity less than 3.
#
#You may assume that each item name will appear only once in
#the list of InventoryItems, and that quantity will always be
#an integer greater than or equal to 0.


#Write your function here!

def condition(instance,a_str,a_int):
    if instance.name == a_str:
        if instance.quantity > a_int:
            return True
    else:
        return False
def sufficient_inventory(instance_list, a_str, a_int):
    for each_instance in instance_list:
        return condition(each_instance, a_str, a_int)




#If you would like, you may implement the InventoryItem class as
#described and use it to test your code. This is not necessary
#to complete the problem, but it may help you debug. If you
#create a InventoryItem class, all you need is a constructor that
#assigns values to two attributes: self.name and self.quantity.



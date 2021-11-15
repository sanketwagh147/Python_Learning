#Imagine you're writing a program to check registration status
#at a conference. The list of registrants comes in the form of
#a list of instances of the Registrant class.
#
#You don't have access to the code for the Registrant class.
#However, you know that it has at least two attributes:
#name (a string) and authorized (a boolean).
#
#Write a function called is_authorized. is_authorized should
#take two parameters: a list of instances of Registrant
#representing the registered individuals, and a name as a
#string.
#
#The function should return True if _any_ instance in the list
#has the same name and an authorized status of True. It should
#return False if either (a) no instance in the list of
#registrants has the same name, or (b) the instance with the
#same name has an authorized status of False.
#
#You should not assume that the list of registrants is sorted
#in any way.
#
#Hint: Beware of registrants who appear in the list twice with
#different values for authorized. If _any_ instance has a
#the value True for authorized, the function should return True.


#Write your function here!
def is_authorized(instance_list, a_str):
    for each_instance in instance_list:
        if each_instance.name == a_str and each_instance.authorized == True:
            return True
    else:
        return False



#If you would like, you may implement the Registrant class as
#described and use it to test your code. This is not necessary
#to complete the problem, but it may help you debug. If you
#create a Registrant class, all you need is a constructor that
#assigns values to two attributes: self.name and self.authorized.



#Imagine you're writing a program to let a customer buy a ticket
#to an event. To do this, you'll write a function called
#buy_ticket. If the ticket the customer wants to buy is available,
#buy_ticket will return the price of the ticket. If it is not
#available, buy_ticket will return False.
#
#buy_ticket will have two parameters: an instance of
#Ticket (the ticket the customer wants to buy), and a list of
#instances of Ticket (the list of currently-available tickets).
#
#You don't have access to the code for the Ticket class. However,
#you know that it has at least three attributes: section (an
#integer), row (a character), and seat (an integer). It also
#has at least one method: get_price, which returns the price of
#the ticket. get_price requires an argument for tax: you'll use
#0.05.
#
#The ticket is available if at least one ticket from the list of
#available tickets has the same section, row, and seat. Otherwise,
#the ticket is not available. If the ticket is available, return
#the result of calling its get_price method with the argument
#0.05. If it is not available, return False.
#
#HINT: You can NOT use the 'in' operator to quickly check if the
#requested ticket is in the available list. I mean, you're
#allowed to try, but it won't work because Python sees different
#instances as different entities even if they have the same
#attributes!


#Write your function here!
def buy_ticet(an_instance, instance_list):
    for each_instance in instance_list:
        if each_instance.section == an_instance.section and each_instance.row == an_instance.row and each_instance.seat == an_instance.seat:
            return each_instance.get_price(0.05)
    return False


#You can do this problem without having direct access to the
#definition of the Ticket class. However, if you would like,
#you may copy your code from Problem 1 here to test your
#function. If you do that, you may uncomment the following lines
#to test your function out; however, you can do this without
#copying in your code from Problem 1. Note that our autograder
#will use our copy of Ticket, not yours; so if your class doesn't
#match the description, your code may work with your class but
#not with ours.
#
#If you do copy/paste in your Ticket class and uncomment these
#lines, they should print 52.5, False, False, False.

#available_ticket_1 = Ticket(140, "A", 15)
#available_ticket_2 = Ticket(140, "A", 16)
#available_ticket_3 = Ticket(210, "F", 37)
#available_ticket_4 = Ticket(210, "F", 38)
#available_tickets = [available_ticket_1, available_ticket_2,
#                     available_ticket_3, available_ticket_4]
#target_ticket_1 = Ticket(140, "A", 15)
#target_ticket_2 = Ticket(130, "A", 15)
#target_ticket_3 = Ticket(210, "G", 37)
#target_ticket_4 = Ticket(210, "F", 15)
#
#print(buy_ticket(target_ticket_1, available_tickets))
#print(buy_ticket(target_ticket_2, available_tickets))
#print(buy_ticket(target_ticket_3, available_tickets))
#print(buy_ticket(target_ticket_4, available_tickets))


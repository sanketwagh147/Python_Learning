#Create a class called Ticket. Ticket should have three
#attributes (instance variables): section, row, and seat.
#Make sure the variable names match those words. section
#and seat will both be integers; row will be a character.
#
#Ticket should have a constructor with three required
#parameters, one for each of those attributes (section,
#row, seat, in that order).
#
#Ticket should also have a method called get_price.
#get_price should have one additional parameter (other
#than self): tax, a decimal representing a sales tax rate
#between 0.01 and 0.10. get_price should return the price
#of the ticket according to the following reasoning:
#
# - If the section is in the 100s (that is, less than 200),
#   the base price is $50.
# - If the section is in the 200s (that is, less than 300),
#   the base price is $30.
# - If the section is in the 300s, the base price is $10.
#
#get_price should return the price (as a float) after tax
#rounded to 2 decimal places; that is, the base price plus
#the product of the tax rate and the base price. You may
#assume the section will be between 100 and 399.
#
#For example, if the section was 140, and the argument to
#get_price was 0.05, then get_price would return 52.5:
#50 + (0.05 * 50).
#
#HINT: Tax rate is NOT an attribute of the object; it is
#an argument only passed into the get_price method.


#Write your class here!
class Ticket:
    section = int
    row = str
    seat = int

    def __init__(self, section, row, seat):
        self.section = section
        self.row = row
        self.seat = seat

    def get_price(self, tax):
        if self.section < 200:
            return 50 + (50 * tax)
        elif self.section < 300:
            return 30 + (30 * tax)
        else:
            return 10 + (10 * tax)



#The code below will test your class. If it works, it
#should print 140, A, 15, and 52.5.
test_ticket = Ticket(140, "A", 15)
print(test_ticket.section)
print(test_ticket.row)
print(test_ticket.seat)
print(test_ticket.get_price(0.05))



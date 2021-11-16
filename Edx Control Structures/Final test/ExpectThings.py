original_total = 20.0
sales_tax_rate = 0.1
is_member = True
has_coupon = True

#You may modify the lines of code above, but don't move them!
#When you Submit your code, we'll change these lines to
#assign different values to the variables.

#Imagine you're writing the software for a cash register at a
#retail vendor. The cash register is given a total by the
#cashier (original_total), and must print the total cost for
#the customer, under the following rules:
#
# - There is currently a "$5 off $15" coupon available. If their
#   original total is more than $15 and they have the coupon
#   (has_coupon), they can use this coupon. If their total is
#   below $15, the value of has_coupon doesn't matter.
# - If the customer is a member of the store's discount
#   program (is_member), they receive a 10% discount.
# - Sales tax should be added. Sales tax is the sales_tax_rate
#   multiplied by the original total.
#
#Note that these changes should be applied in this order: first
#the coupon (if available and eligible), then the customer
#discount, then the sales tax.
#
#For example, if original_total is 20, sales tax is 0.10,
#they have a coupon, and they are members, then their total
#would be:
#
#  $20 - $5 = $15 (coupon)
#  $15 - (0.1 * $15) = $13.50 (customer discount)
#  $13.5 + (0.1 * 13.5) = $14.85 (sales tax)
#
#Write some code that prints the total the customer is expected
#to pay, including the dollar sign, rounded to two decimal places
#(don't worry about the trailing 0 for totals like $15.50).
#
#Hint: To round a number, use the round function. For example,
#round(the_num, 2) will round the_num to two decimal places and
#return the result. Round only on the last step; if you round
#after each calculation, your final result may be off by a cent
#or two.


#Add your code here! Make sure to print the dollar sign, too.
if original_total >15 and has_coupon == True:
    discount = 5
    original_total -= discount
# print(original_total)
if is_member == True:
    discount = (10/100)*original_total
    original_total -= discount
# print(original_total)
print("$"+str(round(original_total + (original_total*sales_tax_rate),2)))









#Imagine you're writing the software for a credit card
#processor. This credit card offers 1% cashback to the
#cardholder, which it calculates by deducting 1%
#directly from the original purchase price. The software
#also needs to account for charges made in different
#currencies; these first need to be converted to the
#account's local currency.
#
#Write a function called calculate_charge.
#calculate_charge will have one positional parameter and
#one keyword parameter. The positional parameter will
#represent the original amount of the charge, in whatever
#currency the charge was performed in. The keyword
#parameter will represent the exchange rate between the
#charge's currency and the account's currency; by default,
#it should be 1.0, meaning that the charge took place in
#the account's own currency.
#
#calculate_charge should return the actual charge that
#should appear on the spender's credit card. This would
#be the charge converted to the account's local currency
#(by dividing the charge amount by the exchange rate) and
#deducting 1%. The result should be rounded to two decimal
#places, but not until after all other calculations are
#made.
#
#For example, right now, 1 US Dollar is worth 0.91 Euros.
#A 20 Euro purchase costs $21.98 because 20 / 0.91 = 21.98.
#1% of 21.98 is 0.2198. So, if the function is called with
#an original price of 20.0 and an exchange rate of 0.91,
#it would return 21.76.
#
#Hint: Remember, you can round a number to two decimal
#places by using the round function. round(the_num, 2) will
#return the_num rounded to two decimal places.


#Add your code here!
def calculate_charge(original_amt, exchange_rate=1.0):
        local_rate = original_amt/exchange_rate
        return round(local_rate - ((1/100)*local_rate),2)



#Below are some lines of code that will test your function.
#You can change the value of the variable(s) to test your
#function with different inputs.
#
#If your function works correctly, this will originally
#print:
#19.8
#21.76
print(calculate_charge(20.0))
print(calculate_charge(20.0, exchange_rate = 0.91))







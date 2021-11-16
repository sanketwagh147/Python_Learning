#Imagine you're writing the code for an intelligent
#temperature device. The device takes a measurement every
#10 seconds. However, some readings may come up invalid.
#We can assume based on operating conditions that all
#valid temperatures will be between 20 and 80.
#
#Write a function called average_temp. average_temp
#should have one parameter, a list of integers. The list
#represents a series of temperature measurements over the
#past several minutes.
#
#average_temp should return the average of all the last
#five _valid_ (greater than or equal to 20, less than or
#equal to 80) measurements.  Round the result to 1
#decimal place (you can use round(some_float, 1) to round
#to 1 decimal place).
#
#For example, if the list of measurements was this:
#
# [5, 62, 72, 102, 68, 75, 73, 3, 7, 79]
#
#average_temp would return 73.4: the last 5 valid
#measurements are (in reverse order) 79, 73, 75, 68, and
#72. (79 + 73 + 75 + 68 + 72) / 5 = 73.4.
#
#If there are fewer than five valid readings, return the
#averages of however many valid readings there are.


#Add your code here!
def average_temp(a_list_of_integers):
    valid_temp = []
    for each_reading in a_list_of_integers:
        if each_reading >= 20 and each_reading <=80:
            valid_temp.append(each_reading)
    # print(valid_temp)
    if len(valid_temp) >= 5:
        return round(sum(valid_temp[-5:])/5, 1)
    else:
        return round(sum(valid_temp)/len(valid_temp), 1)

#Below are some lines of code that will test your function.
#You can change the value of the variable(s) to test your
#function with different inputs.
#
#If your function works correctly, this will originally
#print: 73.4, then 67.0 (on their own lines)
a_list = [5, 62, 72, 102, 68, 75, 73, 3, 7, 79]
print(average_temp(a_list))

a_list_2 = [5, 62, 72, 102]
print(average_temp(a_list_2))




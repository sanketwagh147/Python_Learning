#Write a function called st_dev. st_dev should have one
#parameter, a filename. The file will contain one integer on
#each line. The function should return the population standard
#deviation of those numbers.
#
#The formula for population standard deviation can be found here:
#edge.edx.org/asset-v1:GTx+gt-mooc-staging1+2018_T1+type@asset+block@stdev.PNG
#
#The formula is a bit complex, though, and since this is a
#CS class and not a math class, here are the steps you would
#take to calculate it manually:
#
# 1. Find the mean of the list.
# 2. For each data point, find the difference between that
#    point and the mean. Square that difference, and add it
#    to a running sum of differences.
# 4. Divide the sum of differences by the length of the
#    list.
# 5. Take the square root of the result.
#
#You may assume for this problem that the file will contain
#only integers -- you don't need to worry about invalid
#files or lines. The easiest way to take the square root is
#to raise it to the 0.5 power (e.g. 2 ** 0.5 will give the
#square root of 2).
#
#HINT: You might find this easier if you load all of the
#numbers into a list before trying to calculate the average.
#Either way, you're going to need to loop over the numbers
#at least twice: once to calculate the mean, once to
#calculate the sum of the differences.
#Add your function here!
def st_dev(a_file):
    file = open(a_file, "r")
    contents = file.readlines()
    # print(contents)
    total = 0
    count = 0
    for each_item in contents:
        # print(each_item)
        integer = int(each_item.rstrip("\n"))
        # print(integer)
        total += integer
        count += 1
    mean_of_list = total/count
    # print(mean_of_list)
    sum_of_differences = 0
    for each_item in contents:
        integer = int(each_item.rstrip("\n"))
        difference = integer - mean_of_list
        square_difference = difference* difference
        # print(square_difference)
        sum_of_differences += square_difference
    # print(square_difference)
    divide_by_length = sum_of_differences/len(contents)
    file.close()
    return divide_by_length**0.5
#Below are some lines of code that will test your function.
#You can change the value of the variable(s) to test your
#function with different inputs.
#
#If your function works correctly, this will originally
#print 27.796382658340438 (or something around there).
print(st_dev("some_numbers.txt"))

#edx Sample
#First, we define the function:
def st_dev(filename):

    #And as before, we then open the file:
    file = open(filename)

    #Now we have a choice to make. We know we need to load
    #all the numbers. We could _just_ do that first, then
    #loop over the numbers to calculate the mean... but why
    #not do both at once?
    #
    #First we'll create an empty list to add the numbers
    #to:
    numbers = []

    #Then we'll create a running sum. We don't need to
    #count the numbers manually because we'll know how many
    #are there from the length of the list.
    total = 0

    #Now, we go line-by-line through the file...
    for line in file:

        #First, we convert the current line to an integer:
        this_number = int(line)

        #Then, we add that number to our list:
        numbers.append(this_number)

        #Then we add that number to our running total:
        total += this_number

    #Because we're now done with the file, we should close it:
    file.close()

    #Now, we can go ahead and calculate our mean:
    mean = total / len(numbers)

    #The process of calculating the standard deviation
    #is really just like doing this exact process again,
    #but instead of adding each number, we'll add the
    #squared difference between each number and the mean.
    #That sounds different, but it really isn't. First,
    #we create a sum:
    total_difference = 0

    #Next, we iterate through the numbers:
    for number in numbers:

        #And we add to the total difference -- but instead
        #of adding the number, we add the number minus the
        #mean squared:
        this_difference = (number - mean) ** 2
        total_difference += this_difference

    #Now we have the total of all the differences and the
    #number of items in the list, so we can calculate our
    #result:
    result = (total_difference / len(numbers)) ** 0.5

    #And return it:
    return result


print(st_dev("some_numbers.txt"))




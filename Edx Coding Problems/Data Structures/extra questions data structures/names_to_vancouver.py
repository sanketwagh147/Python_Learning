#Vancouver citation style cites author names like this:
#
#  Last F, Joyner D, Burdell G
#
#Note the following:
#
# - Each individual name is listed as the last name, then a
#   space, then the first initial. No periods or commas within
#   each name.
# - The names are separated by commas, including the last
#   two.
# - There is no space or comma following the last period.
#
#Write a function called names_to_vancouver. names_to_vancouver
#should take as input a list of strings, and return a single
#string according to the style given above. You can assume
#that each item of the list will be a first and last name:
#no middle initials. For example:
#
#  names_to_vancouver(["First Last", "David Joyner", "George Burdell"])
#
#...would return "Last F, Joyner D, Burdell G".


#Write your function below!
def names_to_vancouver(list_of_strings):
    output_list = []
    for each_name in list_of_strings:
        # print(each_name)
        output_list.append(each_name.split()[1] + " " + each_name.split()[0][0])
    # print(output_list)
    return ", ".join(output_list)

#Below are some lines of code that will test your function.
#You can change the value of the variable(s) to test your
#function with different inputs.
#
#If your function works correctly, this will originally
#print: Last F, Joyner D, Burdell G
print(names_to_vancouver(["First Last", "David Joyner", "George Burdell"]))



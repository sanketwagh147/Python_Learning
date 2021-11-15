#Write a function called one_dimensional_booleans.
#one_dimensional_booleans should have two parameters:
#a list of booleans called bool_list and a boolean called
#use_and. You may assume that bool_list will be a list
#where every value is a boolean (True or False).
#
#The function should perform as follows:
#
# - If use_and is True, the function should return True if
#   every item in the list is True (simulating the and
#   operator).
# - If use_and is False, the function should return True if
#   any item in the list is True (simulating the or
#   operator).


#Write your function here!
def one_dimensional_booleans(bool_list, use_and):
    true_count = 0
    for each_item in bool_list:
        if each_item == True:
            true_count += 1
    # print(true_count)
    if use_and == True:
        if true_count == len(bool_list):
            return True
        else:
            return False
    else:
        if true_count >= 1:
            return True
        else:
            return False


#Below are some lines of code that will test your function.
#You can change the value of the variable(s) to test your
#function with different inputs.
#
#If your function works correctly, this will originally
#print: True, False, True, False.
print(one_dimensional_booleans([True, True, True], True))
print(one_dimensional_booleans([True, False, True], True))
print(one_dimensional_booleans([True, False, True], False))
print(one_dimensional_booleans([False, False, False], False))

#
#
# sample Answers

def one_dimensional_booleans(bool_list, use_and):

    #There are a lot of different ways you could do this.
    #You could, for example, loop over each item in the
    #list and update a running result based on the new
    #value.
    #
    #Let's try it a simpler way, though. If use_and was
    #False, then our logic is pretty simple: we just
    #return whether 'True' is anywhere in the list:

    if not use_and:
        return True in bool_list

    #If use_and was True, our logic is just a little bit
    #more complicated. First, we want to find our whether
    #False is in the list. If it is, then we want to
    #return False; if it's not (meaning all the values
    #are True), then we want to return True. So, we want
    #to return the *opposite* of False in bool_list. We
    #can do that with the not operator:

    else:
        return not False in bool_list

    #Note that we could actually compress these four lines
    #down into only one, but it makes the logic a little
    #harder to follow:
    #
    #return (use_and and True in bool_list) or (not use_and and not False in bool_list)



print(one_dimensional_booleans([True, True, True], True))
print(one_dimensional_booleans([True, False, True], True))
print(one_dimensional_booleans([True, False, True], False))
print(one_dimensional_booleans([False, False, False], False))






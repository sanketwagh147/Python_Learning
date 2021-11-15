#Last exercise, you wrote a function called
#one_dimensional_booleans that performed some reasoning
#over a one-dimensional list of boolean values. Now,
#let's extend that.
#
#Imagine you have a two-dimensional list of booleans,
#like this one:
#[[True, True, True], [True, False, True], [False, False, False]]
#
#Notice the two sets of brackets: this is a list of lists.
#We'll call the big list the superlist and each smaller
#list a sublist.
#
#Write a function called two_dimensional_booleans that
#does the same thing as one_dimensonal_booleans. It should
#look at each sublist in the superlist, test it for the
#given operator, and then return a list of the results.
#
#For example, if the list above was called a_superlist,
#then we'd see these results:
#
# two_dimensional_booleans(a_superlist, True) -> [True, False, False]
# two_dimensional_booleans(a_superlist, False) -> [True, True, False]
#
#When use_and is True, then only the first sublist gets
#a value of True. When use_and is False, then the first
#and second sublists get values of True in the final
#list.
#
#Hint: This problem can be extremely difficult or
#extremely simple. Try to use your answer or our
#code from the sample answer in the previous problem --
#it can make your work a lot easier! You may even want
#to use multiple functions.
#Write your function here!
def two_dimensional_booleans(a_list, use_and):
    true_count = 0
    count = 0
    ret_list=[]
    for bool_list in a_list:
        true_count = 0
        for each_item in bool_list:
            if each_item == True:
                true_count += 1
    # print(true_count)
        if use_and == True:
            if true_count == len(bool_list):
                ret_list.append(True)
            else:
                ret_list.append(False)
        if use_and == False:
            if true_count >= 1:
                ret_list.append(True)
            else:
                ret_list.append(False)
    return ret_list


#Below are some lines of code that will test your function.
#You can change the value of the variable(s) to test your
#function with different inputs.
#
#If your function works correctly, this will originally
#print:
#[True, False, False]
#[True, True, False]
bool_superlist = [[True, True, True], [True, False, True], [False, False, False]]
# print(two_dimensional_booleans(bool_superlist, True))
print(two_dimensional_booleans(bool_superlist, False))

#SAmple Answers

#There are two ways we could do this. Let's start with the
#more straightforward one, then you can see the more
#advanced (but also more simple) one in sample_answer_2.py.
#
#Recall our code from the previous problem:
#
#def one_dimensional_booleans(bool_list, use_and):
#    if not use_and:
#        return True in bool_list
#    else:
#        return not False in bool_list
#
#Now, this time instead of returning the result for one
#list, we want to build up a list of results for multiple
#lists. Our end result, however, isn't all that different:

def two_dimensional_booleans(bool_superlist, use_and):

    #First, to build up a list of results, we need to have
    #a list:

    results = []

    #Next, we need to iterate over each sublist in the
    #superlist:

    for bool_sublist in bool_superlist:

        #However, at this point, the problem is identical
        #to the previous problem: for the list we're
        #looking at now (bool_sublist), we want to add
        #its result to results. The actual logic, though,
        #is the same:

        if not use_and:
            results.append(True in bool_sublist)
        else:
            results.append(not False in bool_sublist)

    #Then, once that's all done, we return our list of
    #results:

    return results

    #So, the overall reasoning is the same, it's just that
    #instead of doing it for one list, we iterate over a
    #list of lists and do it for *each* list.
    #
    #However, if the logic is that similar, could we have
    #just used our code from the previous problem? Check out
    #sample_answer_2.py to see!


bool_superlist = [[True, True, True], [True, False, True], [False, False, False]]
print(two_dimensional_booleans(bool_superlist, True))
print(two_dimensional_booleans(bool_superlist, False))

# sample Answers 2

#We could actually solve this problem in only five new
#lines of code by making use of the function we wrote
#before. So, to start, let's copy in our function from
#the previous exercise, one_dimensional_booleans:

def one_dimensional_booleans(bool_list, use_and):
    if use_and:
        return not False in bool_list
    else:
        return True in bool_list

#Now that we have that, our two_dimensional_booleans
#function gets simpler. All we need to do is iterate
#through bool_superlist, call one_dimensional_booleans
#on each list, and add the result to a new list.

def two_dimensional_booleans(bool_superlist, use_and):

    #Like before, we start by creating a list to hold
    #our results:

    results = []

    #And like before, we iterate through each sublist:

    for bool_sublist in bool_superlist:

        #But instead of copying in and modifying our
        #logic from one_dimensional_booleans, we just
        #call it on the current sublist. It takes care
        #of all the logic for us, so we just append
        #the result directly to results:

        results.append(one_dimensional_booleans(bool_sublist, use_and))

    #Then, as before, we return the results.

    return results

    #This is a great example of code reuse and modularity.
    #By keeping functions small and targeted, we raise the
    #likelihood we can reuse them for multiple purposes.



bool_superlist = [[True, True, True], [True, False, True], [False, False, False]]
print(two_dimensional_booleans(bool_superlist, True))
print(two_dimensional_booleans(bool_superlist, False))






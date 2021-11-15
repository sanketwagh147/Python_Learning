#Write a function called write_weird_file. write_weird_file
#should take two positional parameters. The first should be
#a filename, and the second should be a list. The function
#should also have three keyword parameters: mode, sort_first
#and reverse_first. The default value for mode should be "w",
#and the default values for both sort_first and reverse_first
#should be False.
#
#write_weird_file should write the contents of the list to
#the given filename. Each item from the list should be on a
#separate line. The list items could be strings, floats,
#characters, or integers. If the mode is "w", it should
#overwrite the current contents; if the mode is "a", it
#should append to the current contents. You may assume there
#will be no other value for mode.
#
#If sort_first is True, it should sort the list before
#writing. If reverse_first is True, then it should reverse
#the list before writing. If both are True, it should sort,
#then reverse.
#Add your function here!
def write_weird_file(a_file_name, a_list, mode="w", sort_first=False, reverse_first=False):

    if mode == "w":
        file = open(a_file_name, "w")
        str_list = [str(inte) for inte in a_list]
        if sort_first == True:
            str_list.sort()
        if reverse_first == True:
            str_list.reverse()
        # print(str_list)
        for each_item in str_list:
            file.write(each_item+"\n")
        file.close()

    if mode == "a":
        file = open(a_file_name, "a")
        str_list = [str(inte) for inte in a_list]
        if sort_first == True:
            str_list.sort()
        if reverse_first == True:
            str_list.reverse()
        for each_item in str_list:
            file.write(each_item+"\n")
        file.close()

#EDx Sample
#First, we define the function. This one is more complicated
#because it has both positional and keyword parameters.
#So, the function definition would look like this:
def write_weird_file(filename, content, mode="w", sort_first=False, reverse_first=False):

    #Next, we open the file. Note that because the only two
    #values we were told to expect for mode were "w" and
    #"a", we can just pass mdoe directly into the open
    #function:
    the_file = open(filename, mode)

    #Next, we want to check both possible changes we might
    #make to the list, sort and reverse:
    if sort_first:
        content.sort()
    if reverse_first:
        content.reverse()

    #Finally, we iterate through the list of content,
    #writing each item to the file:
    for item in content:
        print(item, file=the_file)

    #And then close the file:
    the_file.close()



write_weird_file("output.txt", ["Hmm, I bet this text will disappear.", "I wonder where it will go?"])
write_weird_file("output.txt", ["Wait, where'd the other text go?", "It's gone!"])
write_weird_file("output.txt", [2, 1, 3], mode="a", sort_first=True, reverse_first=True)







#Below are some lines of code that will test your function.
#You can change the value of the variable(s) to test your
#function with different inputs.
#
#If your function works correctly, this will originally
#print nothing. However, if you open the file called
#output.txt in the top left after running it, the contents
#of the file should be:
#Wait, where'd the other text go?
#It's gone!
#3
#2
#1
write_weird_file("output.txt", ["Hmm, I bet this text will disappear.", "I wonder where it will go?"])
write_weird_file("output.txt", ["Wait, where'd the other text go?", "It's gone!"])
write_weird_file("output.txt", [2, 1, 3], mode="a", sort_first=True, reverse_first=True)






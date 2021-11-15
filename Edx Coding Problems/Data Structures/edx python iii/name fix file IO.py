#You've been sent a list of names. Unfortunately, the names
#come in two different formats:
#
#First Middle Last
#Last, First Middle
#
#You want the entire list to be the same. For this problem,
#we'll say you want the entire list to be First Middle Last.
#
#Write a function called name_fixer. name_fixer should have two
#parameters: an output filename (the first parameter) and the
#input filename (the second parameter). You may assume that every
#line will match one of the two formats above: either First Middle
#Last or Last, First Middle.
#
#name_fixer should write to the output file the names all
#structured as First Middle Last. If the name was already structured
#as First Middle Last, it should remain unchanged. If it was
#structured as Last, First Middle, then Last should be moved
#to the end after a space and the comma removed.
#
#The names should appear in the same order as the original file.
#
#For example, if the input file contained the following lines:
#David Andrew Joyner
#Hart, Melissa Joan
#Cyrus, Billy Ray
#
#...then the output file should contain these lines:
#David Andrew Joyner
#Melissa Joan Hart
#Billy Ray Cyrus


#Add your code here!
def name_fixer(output_file, input_file):
    list1 = []
    for lines in open(input_file):
        list1.append(lines.strip())
        # print(list1)
        # lol = "".join(list1)
        # print(lol)
        # list1.append(lol)
    # print(list1)
    a_list_of_string = list1
    for each_name in a_list_of_string:
        # print(each_name)
        if "," not in each_name:
            pass
        else:
            each_name_list=each_name.split()
            # print(each_name_list)
            modified_list=[each_name_list[2],each_name_list[0],each_name_list[1]]
            # print(modified_list)
            name_string=modified_list[2]+","+" "+modified_list[0]+" "+ modified_list[1]
            # print(name_string)
            # name_string="".join(name_string)
            # print(name_string)
            # print(type(name_string))
            name_string=name_string.replace(",", "")
            # print(name_string)
            index_to_be_removed=a_list_of_string.index(each_name)
            # print(index_to_be_removed)
            del a_list_of_string[index_to_be_removed]
            # print(a_list_of_string)
            a_list_of_string.insert(index_to_be_removed, name_string)
            # print(a_list_of_string)
            # a_list_of_string_2 = "".join(name_string)
    # print(a_list_of_string)
    file = open(output_file, "w")
    a_list_of_string = map(lambda x: x + '\n', a_list_of_string)
    # print(a_list_of_string)
    file.writelines(a_list_of_string)
    file.close()
    return a_list_of_string
#The code below will test your function. You can find the two
#files it references in the drop-down in the top left. If your
#code works, output_file.txt should have the text:
#David Andrew Joyner
#Melissa Joan Hart
#Billy Ray Cyrus
name_fixer("output_file.txt", "input_file.txt")
print("Done running! Check output_file.txt for the result.")

#If you accidentally erase input_file.txt, here's its original
#text to copy back in (remove the pound signs):
#David Andrew Joyner
#Hart, Melissa Joan
#Cyrus, Billy Ray



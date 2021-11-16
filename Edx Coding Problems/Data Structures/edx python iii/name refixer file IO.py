#You've been sent a list of names. Unfortunately, the names
#come in two different formats:
#
#First Middle Last
#Last, First Middle
#
#You want the entire list to be the same. For this problem,
#we'll say you want the entire list to be Last, First Middle.
#
#Write a function called name_refixer. name_refixer should have two
#parameters: an output filename (the first parameter) and the
#input filename (the second parameter). You may assume that every
#line will match one of the two formats above: either First Middle
#Last or Last, First Middle.
#
#name_refixer should write to the output file the names all
#structured as Last, First Middle. If the name was already structured
#as Last, First Middle, it should remain unchanged. If it was
#structured as First Middle Last, then Last should be moved
#to the front and a comma should be added after it.
#
#The names should appear in the same order as the original file.
#
#For example, if the input file contained the following lines:
#David Andrew Joyner
#Hart, Melissa Joan
#Cyrus, Billy Ray
#
#...then the output file should contain these lines:
#Joyner, David Andrew
#Hart, Melissa Joan
#Cyrus, Billy Ray


#Add your code here!
def name_refixer(output_file, input_file):
    list1 = []
    for lines in open(input_file):
        list1.append(lines.strip())
      # print(list1)
    a_list_of_string = list1
    # print(a_list_of_string)
    for each_name in a_list_of_string:
        # print(each_name)
        if "," in each_name:
            pass
        else:
            each_name_list=each_name.split()
            # print(each_name_list)
            modified_list=[each_name_list[2],each_name_list[0],each_name_list[1]]
            # print(modified_list)
            name_string=modified_list[0]+","+" "+modified_list[1]+" "+ modified_list[2]
            # print(name_string)
            index_to_be_removed=a_list_of_string.index(each_name)
            # print(index_to_be_removed)
            del a_list_of_string[index_to_be_removed]
            # print(a_list_of_string)
            a_list_of_string.insert(index_to_be_removed, name_string)
            # print(a_list_of_string)
    # return a_list_of_string
    file = open(output_file, "w")
    a_list_of_string = map(lambda x: x + '\n', a_list_of_string)
    # print(a_list_of_string)
    file.writelines(a_list_of_string)
    file.close()
    return a_list_of_string

#The code below will test your function. You can find the two
#files it references in the drop-down in the top left. If your
#code works, output_file.txt should have the text:
#Joyner, David Andrew
#Hart, Melissa Joan
#Cyrus, Billy Ray
name_refixer("output_file.txt", "input_file.txt")
print("Done running! Check output_file.txt for the result.")

#If you accidentally erase input_file.txt, here's its original
#text to copy back in (remove the pound signs):
#David Andrew Joyner
#Hart, Melissa Joan
#Cyrus, Billy Ray



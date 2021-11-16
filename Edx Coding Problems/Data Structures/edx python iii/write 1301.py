#Write a function called write_1301 which will write a file
#in the format described in Coding Problem 4.4.2. The
#sample.cs1301 file has been included to refresh your
#memory. Your function should accept two arguments:
#A string of a filename to write to, and a list of tuples.
#You can assume that each tuple will have the following
#format:
#
#(int, str, int, int, float)
#
#Each tuple will represent a line in the file, and each
#item in the tuple should correspond to the
#assignment number, the assignment name, the student's
#grade, the total possible number of points, and the
#assignment weight respectively.


#Write your function here!
def write_1301(output_file, a_tuple_list):
    file = open(output_file, "w")
    # print(a_tuple_list)
    a_list = list(a_tuple_list)
    # print(a_list)
    # file.writelines(a_tuple_list)
    for each_tuple in a_list:
        # print(each_tuple)
        new_list = [str(each_item)+" " for each_item in each_tuple]
        new_list[-1] = new_list[-1].strip()
        # print(remove_space)
        # new_list.append(new_list[-1])
        file.writelines(new_list)
        file.write("\n")
        print(new_list)
    file.close()



#The code below will test your function. It's not used
#for grading, so feel free to modify it! You may check
#output.cs1301 to see how it worked.
tuple1 = (1, "exam_1", 90, 100, 0.6)
tuple2 = (2, "exam_2", 95, 100, 0.4)
tupleList = [tuple1, tuple2]
write_1301("output.cs1301", tupleList)


# EDX sample Answer

def write_1301(filename, tuple_list):

    #Like the last problem, this problem can be done
    #very easily, or it can be more difficult. Don't
    #worry if it took you a while to get -- it just
    #takes practice!
    #
    #To start, we want to open the file in write
    #mode:

    file_writer = open(filename, "w")

    #Next, we want to go through each tuple in the
    #list. These tuples will each become a line in
    #the file, so we'll use 'line' as our loop
    #variable:

    for line in tuple_list:

        #line will be a tuple with five items, and
        #we want to print each one to the file
        #separated by spaces.  However, they're not
        #all strings, so we can't use
        #" ".join(tuple_list).
        #
        #Instead, we'll just do this one part at a
        #time. To make this easier to follow, let's
        #unpack the tuple first:

        number, name, grade, max_grade, weight = line

        #Now let's print each of these parts to the
        #file, separated by spaces:

        file_writer.write(str(number) + " ")
        file_writer.write(name + " ")
        file_writer.write(str(grade) + " ")
        file_writer.write(str(max_grade) + " ")
        file_writer.write(str(weight) + "\n")

    #Then, once we're all done, we close the file.

    file_writer.close()


tuple1 = (1, "exam_1", 90, 100, 0.6)
tuple2 = (2, "exam_2", 95, 100, 0.4)
tupleList = [tuple1, tuple2]
write_1301("output.cs1301", tupleList)









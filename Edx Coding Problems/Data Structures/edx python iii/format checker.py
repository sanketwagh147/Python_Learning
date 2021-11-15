#This is a long one -- our answer is 20 lines of code, but
#yours will probably be longer. That's because it's one of the
#more authentic problems we've done so far. This is a real
#problem you'll start to face if you want to start creating
#useful programs.
#
#One of the reasons that filetypes work is that everyone
#agrees how they are structured. A ".png" file, for example,
#always contains "PNG" in the first four characters to
#assure the program that the file is actually a png. If these
#standards were not set, it would be hard to write programs
#that know how to open and read the file.
#
#Let’s define a new filetype called ".cs1301".
#In this file, every line should be structured like so:
#
#number assignment_name grade total weight
#
#In this file, each component will meet the following
#description:
#
# - number: an integer-like value of the assignment number
#
# - assignment_name: a string value of the assignment name
#
# - grade: an integer-like value of a student’s grade
#
# - total: an integer-like value of the total possible
#   number of points
#
# - weight: a float-like value ranging from 0 to 1
#   representing the percent of the student’s grade this
#   assignment is worth. All the weights should add up to 1.
#
#Each component should be separated with exactly one space.
#A good sample file is available to view as
#"sample.cs1301".
#
#Write a function called format_checker that accepts a
#filename and returns True if the file contents accurately
#conform to the described format. Otherwise the function
#should return False. In other words, it should return True
#if:
#
# - Each line has five elements separated by spaces, AND
# - The first, third, and fourth elements are integers, AND
# - The fifth element is a decimal number, AND
# - All the fifth elements add to 1.
#
#You can make changes to test.cs1301 to test your function,
#or test it with sample.cs1301. Right now, running it on
#sample.cs1301 should return True, and on test.cs1301
#should return False.
#
#Hint 1: .split() will likely help separate each line into
#its components.
#Hint 2: .split() returns a list. So, if you were to do
#something like say split_line = line.split(), then
#split_line[0] would give the first item, split_line[1] would
#give the second item, etc.
#Hint 3: If you're having trouble, try breaking it down by
#parts. First check the file to see if it has the right
#number of items per line, then whether the items are of
#the correct type, then whether the fifth elements add to
#1. Remember, you know how to do each individual check
#(checking types, adding numbers, finding list lengths) --
#the hard part is knitting this all together into one bigger
#solution.


#Write your function here!
def format_checker(a_file_under_test):
    list_of_lines = []
    count = 0
    for lines in open(a_file_under_test):
        list_of_lines.append(lines.strip())
    # print(list_of_lines)
    for each_item in list_of_lines:
        # print(each_item)
        each_line_list = each_item.split()
        # print(each_line_list)
        # fifth_item_list = [item[3] for item in each_line_list]
        # print(fifth_item_list)
        # print(count)
        try:
            first_item = each_line_list[0]
            third_item = each_line_list[2]
            fourth_item = each_line_list[3]
            fifth_item = each_line_list[4]
            # count += float(fifth_item)
            # print(fifth_item)
            # print(first_item, end=" ")
            # print(third_item, end=" ")
            # print(fourth_item)
            # print(fifth_item)

            fifth_item_as_float = float(fifth_item)
            count +=fifth_item_as_float
            if len(each_line_list) != 5:
                print(len(each_line_list),"condition length not Satisfied")
                return False
            elif first_item.isdigit()==False or third_item.isdigit()==False or fourth_item.isdigit()==False:
                print(first_item, third_item, fourth_item, end= " :")
                print("Condition isdigit not satisfied")
                return False
                    # count += 1
                    # print(fifth_item)
                    # print(type(fifth_item))
                    # print(fifth_item_as_float)
            elif "." not in fifth_item:
                # print(fifth_item, end=" :")
                # print("condtion is decimal not satisfied")
                return False
        except IndexError:
            return False
        finally:
            open(a_file_under_test).close()
    # print(count)
    if count ==1:
        return True
    else:
        return False
        #     # print(count)
#Test your function below. With the original values of these
#files, these should print True, then False:
print(format_checker("sample_1.cs1301"))
print(format_checker("sample_2.cs1301"))

EDX sample
#This is a long problem, but it's made out of a bunch of
#things we know how to do. So, let's break it up.

def format_checker(filename):

    #First, we need to open the file, of course.

	file_reader = open(filename)

    #Next, we know we're going to need to add up all the
    #weights. So, let's go ahead and create that counter
    #and set it to 0.

	total_weight = 0

    #Now, we want to iterate through all the lines in the
    #file and check them one by one.

	for line in file_reader:

        #First, let's split it up into its parts. We know
        #that spaces mark different pieces.

		parts = line.split(" ")

        #The first requirement in our file format is that
        #there by 5 parts on each line. If this line does
        #not have exactly 5 parts, we're done! This isn't
        #a valid line, and only one invalid line makes the
        #entire file invalid.

        if len(parts) != 5:

            file_writer.close()
			return False

        #Next, let's check to make sure each individual
        #part is of the right type. The first, third, and
        #fourth parts should be integers, and the 5th part
        #should be a float. If any of those conversions
        #cause an error, we're done!

		try:
			int(parts[0])
			int(parts[2])
			int(parts[3])
			float(parts[4])

            #Assuming all those conversions work, we now
            #want to add the fourth part to our running
            #total_weight variable.

			total_weight += float(parts[4])
		except:

            #If any of those conversions caused an error,
            #we're done. One error means this line is
            #invalid, and if this line is invalid, the
            #entire file is invalid.

            file_writer.close()
			return False


    #We're now done reading the file, so we can close it:
    file_writer.close()

    #If we reach this part of the function, it means that
    #none of the previous 'return False' lines ran. So,
    #that means we know that each line has 5 parts, and each
    #part of each line is the right type. The only thing we
    #have left to check is whether or not all those total
    #weights added to 1. If they don't, we return False.

    if total_weight != 1:
		return False

    #The only way this next line is reached is if all previous
    #checks were valid: five items per line, correct data
    #types, and weights that add to 1. If any of those were
    #not true, then a 'return False' line would have run. So,
    #we can safely return True.

	return True


print(format_checker("sample.cs1301"))
print(format_checker("test.cs1301"))








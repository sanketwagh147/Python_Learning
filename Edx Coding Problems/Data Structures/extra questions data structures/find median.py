#Write a function called find_median. find_median
#should take as input a string representing a filename.
#The file corresponding to that filename will be a list
#of integers, one integer per line. find_median should
#return the median of the numbers in the file.
#
#If there is an odd number of values in the file, then
#find_median will return the middle value from the numbers
#in the file after they're sorted.
#
#If there is an even number of values in the file, then
#find_median should return the average of the two middle
#values after they're sorted.
#
#For example, in the dropdown in the top left you'll find a
#file named FindMedianInput.txt. There are 19 numbers in
#this file, so the median is the value at index 10 after
#sorting them: 16.
#
#You may assume that all lines in the file will contain a
#positive integer (greater than 0). There may be duplicates.


#Write your function here!
def find_median(a_filename):
    import statistics
    data_from_file = open(a_filename, "r")
    data = data_from_file.read()
    # print(data)
    data_list = data.splitlines()

    # print(data_list)
    data_num_list = [int(i) for i in data_list]
    data_num_list.sort()
    # print(data_num_list)
    # print(len(data_num_list))
    data_from_file.close()
    median1 = statistics.median(data_num_list)
    # if len(data_num_list) % 2 == 0:
    #     # print("even")
    #     median1 = statistics.median(data_num_list)
    #     # number_1 = int(len(data_num_list)/2)
    #     # number_2 = int((len(data_num_list)+1)/2)
    #     # print(data_num_list[number_1])
    #     # print(data_num_list[number_2])
    #     # average = (number_1 + number_2)/2
    #     # # print(average)
    #     return median1
    # else:
    #     # print("odd")
    #     center = (len(data_list)+1)/2
    #     # print(center)
    #     # print(data_num_list)
    #     return data_num_list[int(center)]
    return median1

#Below are some lines of code that will test your function.
#You can change the value of the variable(s) to test your
#function with different inputs.
#
#If your function works correctly, this will originally
#print: 16
print(find_median("FindMedianInput.txt"))



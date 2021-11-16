#We've given you a file called "top500.txt" which contains
#the name and lifetime gross revenue of the top 500
#films at the time this question was written.
#
#Each line of the given file is formatted like so:
# <name>\t<gross revenue in dollars>
#
#In other words, you should call .split("\t") to split
#the line into the movie name (the first item) and the
#gross (the second item).
#
#Unfortunately, these movies are not in order. Write a
#function called "sort_films" that accepts two parameters:
#a string of a source filename and a string of a
#destination filename. Your function should open the
#source file and sort the contents from greatest gross
#revenue to least gross revenue, and write the sorted
#contents to the destination filename. You may assume the
#source file is correctly formatted.
#
#Hint: one common issue on this problem is that every line
#in the input file ends with a line break except the last
#one. If the autograder gives you an index error, open
#top500result.txt and make sure there are 500 lines in your
#output file!


#Write your function here!
# def Sort(sub_li):
#     l = len(sub_li)
#     for i in range(0, l):
#         for j in range(0, l-i-1):
#             if (sub_li[j][1] > sub_li[j + 1][1]):
#                 tempo = sub_li[j]
#                 sub_li[j]= sub_li[j + 1]
#                 sub_li[j + 1]= tempo
#     print(sub_li)
#     print(sub_li)
#     return sub_li
def Sort(sub_li):

    # reverse = None (Sorts in Ascending order)
    # key is set to sort using second element of
    # sublist lambda has been used
    sub_li.sort(key = lambda x: x[1],reverse=True)
    return sub_li

def sort_films(input_file, output_file):
    file = open(input_file, "r")
    movie_list = file.readlines()
    # print(movie_list)
    file.close()
    master_list = []
    return_list = []
    # for i in range(0, len(movie_list)):
    #     each_item = movie_list[i]
    #     each_list = each_item.split("\t")
    #     print(each_list)

    for each_item in movie_list:
        # print(each_item)
        each_list = each_item.split("\t")
        # print(each_list)
        earnings_instr= each_list[1]
        earning_in_int = (int(earnings_instr))
        # print(earning_in_int)
        each_list.append(earning_in_int)
        # print(each_list)
        del each_list[1]
        # print(each_list)
        master_list.append(each_list)
        sub_li = master_list
        return_list = Sort(sub_li)
        out = open(output_file, "w")
        for it in return_list:
            # print(it)
            for every in it:
                # print(every)
                out.write(str(every)+"\t")
            out.write("\n")
            # out.write(it)
        #
        # out.close()
    print(return_list)
    return return_list
#The line of code below will test your function and put
#your results in top500result.txt. Then, it will print
#"Done!"
sort_films("top500.txt", "top500result.txt")
print("Done!")



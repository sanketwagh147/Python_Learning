#A common problem in academic settings is plagiarism
#detection. Fortunately, software can make this pretty easy!
#
#In this problem, you'll be given two files with text in
#them. Write a function called check_plagiarism with two
#parameters, each representing a filename. The function
#should find if there are any instances of 5 or more
#consecutive words appearing in both files. If there are,
#return the longest such string of words (in terms of number
#of words, not length of the string). If there are not,
#return the boolean False.
#
#For simplicity, the files will be lower-case text and spaces
#only: there will be no punctuation, upper-case text, or
#line breaks.
#
#We've given you three files to experiment with. file_1.txt
#and file_2.txt share a series of 5 words: we would expect
#check_plagiarism("file_1.txt", "file_2.txt") to return the
#string "if i go crazy then". file_1.txt and file_3.txt
#share two series of 5 words, and one series of 11 words:
#we would expect check_plagiarism("file_1.txt", "file_3.txt")
#to return the string "i left my body lying somewhere in the
#sands of time". file_2.txt and file_3.txt do not share any
#text, so we would expect check_plagiarism("file_2.txt",
#"file_3.txt") to return the boolean False.
#
#Be careful: there are a lot of ways to do this problem, but
#some would be massively time- or memory-intensive. If you
#get a MemoryError, it means that your solution requires
#storing too much in memory for the code to ever run to
#completion. If you get a message that says "KILLED", it
#means your solution takes too long to run.


#Add your code here!
def check_plagiarism(first_file, second_file):
    dict_1 = {}
    file1 = open(first_file, "r")

    for text in file1:
        list1 = text.split()
        for i in range(0, len(list1) - 5):
            if list1[i] not in dict_1:
                dict_1[list1[i]] = []
            dict_1[list1[i]].append(list1[i+1:i+5])
    file1.close()
    ret_list = []
    file2 = open(second_file, "r")
    for text in file2:
        list1 = text.split()
        for i in range(0, len(list1) - 5):
            if list1[i] in dict_1:
                if list1[i+1:i+5] in dict_1[list1[i]]:
                    j = i + 5
                    k = i + 1
                    # print(list1[k:j+1],dict_1[list1[k]])
                    while(list1[k+1:j+1] in dict_1[list1[k]]):
                        k+=1
                        j+=1
                        if (j == len(list1)):
                            break
                    if(len(list1[i:j]) > len(ret_list)):
                        ret_list = list1[i:j]

    file2.close()
    if len(ret_list) == 0:
        return False
    else:
        return " ".join(ret_list)

#Below are some lines of code that will test your function.
#You can change the value of the variable(s) to test your
#function with different inputs.
#
#If your function works correctly, this will originally
#print:
#if i go crazy then
#i left my body lying somewhere in the sands of time
#False
print(check_plagiarism("file_1.txt", "file_2.txt"))
print(check_plagiarism("file_1.txt", "file_3.txt"))
print(check_plagiarism("file_2.txt", "file_3.txt"))
#
# def check_plagiarism(a_file1, a_file2):
#     file1 = open(a_file1, "r")
#     file2 = open(a_file2, "r")
#     text1_list = file2.read().split()
#     text2_list= file1.read().split()
#     print(text2_list)
#     print(text1_list)
#     duplicate_counter = 0
#     duplicate_list1 = []
#     duplicate_list2 = []
#     # print(text1_list[41])
#     for i in range(0, len(text1_list)):
#         for j in range(0, len(text2_list)):
#             if text1_list[i] == text2_list[j]:
#                 duplicate_list1.append(i)
#                 duplicate_list2.append(j)
#     duplicate_list1.sort()
#     duplicate_list2.sort()
#     print(duplicate_list1)
#     set1 = set(duplicate_list1)
#     set2 = set(duplicate_list2)
#     set1_sorted = sorted(set1)
#     set2_sorted = sorted(set2)
#     # print(set2)
#     main_listy1 = list(set1_sorted)
#     main_listy2 = list(set2_sorted)
#     # print(main_listy1)
#     # print(main_listy2)
#     s = main_listy1
#     maxrun = -1
#     rl = {}
#     for x in s:
#         run = rl[x] = rl.get(x-1, 0) + 1
#         # print(x-run+1, 'to', x)
#         if run > maxrun:
#             maxend, maxrun = x, run
#     # print(range(maxend-maxrun+1, maxend+1))
#     # print(maxrun)
#     if maxrun >= 5:
#         start = maxend-maxrun+1
#         print(start)
#         print(maxend)
#         ret_list=[]
#         for i in range(start, maxend+1):
#             # print(i)
#             ret_list.append(text1_list[i])
#         return " ".join(ret_list)
#     else:
#         return False


#Below are some lines of code that will test your function.
#You can change the value of the variable(s) to test your
#function with different inputs.
#
#If your function works correctly, this will originally
#print:
#if i go crazy then
#i left my body lying somewhere in the sands of time
#False
# print(check_plagiarism("file_1.txt", "file_2.txt"))
# print(check_plagiarism("file_1.txt", "file_3.txt"))
# print(check_plagiarism("file_2.txt", "file_3.txt"))
#
#
#


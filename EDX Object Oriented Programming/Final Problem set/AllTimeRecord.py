#Let's try out a sort of data analysis-style problem. In
#this problem, you're going to have access to a data set
#covering Georgia Tech's all-time football history. The data
#will be a CSV file, meaning that each line will be a comma-
#separated list of values. Each line will describe one game.
#The columns, from left-to-right, are:
#
# - Date: the date of the game, in Year-Month-Day format.
# - Opponent: the name of the opposing team
# - Location: Home, Away, or Neutral
# - Points For: Points scored by Georgia Tech
# - Points Against: Points scored by the opponent
#
#If Points For is greater than Points Against, then Georgia
#Tech won the game. If Points For is less than Points Against,
#then Georgia Tech lost the game. If the two are equal, then
#the game was a tie.
#
#You can see a subsection of this dataset in season2016.csv
#in the top left, but the actual dataset you'll be accessing
#here will have 1237 games.
#
#Write a function called all_time_record. all_time_record
#should take as input a string representing an opposing team
#name. It should return a string representing the all-time
#record between Georgia Tech and that opponent, in the form
#Wins-Losses-Ties. For example, Georgia Tech has beaten
#Clemson 51 times, lost 28 times, and tied 2 times. So,
#all_time_record("Clemson") would return the string "51-28-2".
#
#We have gone ahead and started the function and opened the
#file for you. The first line of the file are headers:
#Date,Opponent,Location,Points For,Points Against. After that,
#every line is a game.


def all_time_record(opponent):
    # record_file = open('../resource/lib/public/georgia_tech_football.csv', 'r')
    record_file = open('season2016.csv', 'r')
    data = record_file.read().splitlines()
    record_list = data[1:]
    record_list1 = []
    # print(data)
    # print(record_list)
    record_dict ={}
    win = 0
    loss = 0
    tie = 0
    record_file.close()
    for each in record_list:
        # print(each)
        list1= each.split(",")
        # print(list1)
        record_list1.append(list1)
    for each in record_list1:
        # print(each)
        # print(each[1])
        if each[1] not in record_dict.keys():
            record_dict[each[1]]=[0,0,0]
            if int(each[3]) > int(each[4]):
                record_dict[each[1]][0] +=1
            elif int(each[3]) < int(each[4]):
                record_dict[each[1]][1] +=1
            else:
                record_dict[each[1]][2] +=1
        else:
            if int(each[3]) > int(each[4]):
                record_dict[each[1]][0] +=1
            elif int(each[3]) < int(each[4]):
                record_dict[each[1]][1] +=1
            else:
                record_dict[each[1]][2] +=1

        # print(each[1])
        # print(each)
        # if each[3] > each[4]:
        #     record_dict[each[1][0]] +=1
    # print(record_dict)
    # record_dict ={}
    # print(list1)
    # for each in list1:
    #     record_dict[each]=[0, 0 ,0]
    #     # print(record_dict)
    ret_list = record_dict[opponent]
    ret_list2 = [str(i) for i in ret_list]
    # print(ret_list)
    return "-".join(ret_list2)
    #Add some code here! Don't forget to close the file when
    #you're done reading from it, before returning.


#Below are some lines of code that will test your function.
#You can change the value of the variable(s) to test your
#function with different inputs.
#
#If your function works correctly, this will originally
#print: 51-28-2, 51-33-1, and 29-21-3, each on a separate
#line.
print(all_time_record("Kentucky"))
# print(all_time_record("Duke"))
# print(all_time_record("North Carolina"))
#




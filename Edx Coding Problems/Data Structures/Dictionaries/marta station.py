#In this problem, we're giving you a file containing some real data from
#the Marta (Atlanta's subway system) database. Each line of the file is
#a record of a single ride at a specific Marta station. Riders enter and
#exit the subway system by tapping a Breeze Card against a gate at a
#specific station.
#
#You can see a preview of what the file will look like in
#marta_sample.csv in the dropdown in the top left. Note, however, that
#the real dataset is massive: over 200,000 individual rides are recorded.
#So, you're going to be dealing with some pretty big data!
#
#Each line of the file contains six items, separated by commas:
#
# - the transit day, in MM/DD/YYYY format.
# - the transit time, in HH:MM:SS format.
# - the device ID, an identifer of the gate at which the rider entered.
# - the station ID, a numeric identifier the station.
# - the use type, whether the rider was entering, exiting, etc.
# - a serial number, the unique identifier of the rider's Breeze Card.
#
#Your goal is to use this file to answer three questions:
#
# - What is the average number of Breeze Card taps per station?
# - What is the station ID of the station whose traffic is the closest
#   to that average?
# - What station has the least overall amount of traffic?
#
#Note that you will answer these questions in the fill-in-the-blank
#problems below, _not_ in this coding exercise. So, you don't have to
#programmatically find the station ID closest to the average: you could
#just print all the stations and their averages, then visually check
#which is closest to the average.
#
#To get you started, we've gone ahead and opened the file:
import collections
import bisect

marta_file = open(r'/Edx Coding Problems/Data Structures/Dictionaries/sample.csv', 'r')
contnents = marta_file.read()
# print(contnents)
# print(type(contnents))
listy = contnents.split("\n")
# print(listy)
# print(type(listy))
data_dict ={}
for each_item in range(0, len(listy)-1):
    # print(listy[each_item])
    # print(type(listy[each_item]))
    mini_listy = listy[each_item].split(",")
    # print(mini_listy)
    station_id = mini_listy[3]
    # print(station_id)
    if station_id in data_dict.keys():
        data_dict[station_id] +=1
        pass
    else:
        data_dict[station_id] = 1
# print( data_dict)
total_taps = sum(data_dict.values())
# print(total_taps)
len_of_dict = len(data_dict)
# print(len_of_dict)
avg = total_taps/len_of_dict
# print(avg)
print((key,value) for data_dict.items())
# res = bisect.bisect_left(list(data_dict.keys()), str(avg))
# print(res)

# # initializing dictionary
# # test_dict = {13 : 'Hi', 15 : 'Hello',  16 : 'Gfg'}
#
# # initializing nearest key
# # search_key = 15.6
#
# # printing original dictionary
# # print("The original dictionary is : " + str(data_dict))
#
# # Using list comprehension + keys() + lambda
# # Closest key in dictionary
# res = data_dict.get(avg) or data_dict[min(data_dict.keys(), key = lambda key: abs(key-avg))]
#
# # printing result
# print("The value to the closest key : " + str(res))
# # for (key, values) in data_dict.items():
#     # print(key,values)


#You may add whatever code you want from here on to answer those three
#questions.
#
#HINT: although there are six items on each line of the file, you only
#need one of them: station ID. If you use split(",") to split up each
#line, station ID will be at index 3 on the list.
#
#HINT 2: You'll probably want to use a dictionary, with station IDs as
#the keys and








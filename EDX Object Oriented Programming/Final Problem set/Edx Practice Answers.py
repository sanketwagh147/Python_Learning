from datetime import datetime
record_file = open('spring2016.csv', 'r')
data = record_file.read().splitlines()
record_list = data[1:]
record_list1 = []
# print(data)
# print(record_list)

record_file.close()
oldest_match = ""
record_list2 =[]
for i in range(0, len(record_list)):
    tuple1 = ()
    # print(type(record_list[0][:10]))
    current_match_list = record_list[i].split(",")
    current_match_date = current_match_list[0]
    current_match_opponent = current_match_list[1]
    current_match_location = current_match_list[2]
    current_match_gtech = current_match_list[3]
    current_match_vs = current_match_list[4]
    # print(current_match_list)
    # print(current_match_date)
    # print(current_match_opponent)

    current_match_date_object = datetime.strptime(current_match_date,"%Y-%m-%d").date()
    tuple1=(current_match_date_object, current_match_opponent,current_match_location,current_match_gtech,current_match_vs)
    record_list2.append(tuple1)
# print(record_list2)
# differential_list = []
# for i in range(0, len(record_list2)):
#     append_list=[]
#     differential = int(record_list2[i][3])-int(record_list2[i][4])
#     append_list = [differential,i]
#     differential_list.append(append_list)
# print(differential_list)
# max1 = max(differential_list)
# print(max1)
opponent = {}

for i in range(0,len(record_list2)):
    # print(record_list2[i][1])
    if record_list2[i][1] not in opponent.keys():
        differential = int(record_list2[i][3]) - int(record_list2[i][4])
        num_games = 1
        opponent[record_list2[i][1]]=[differential, num_games]
        #opponent[record_list2[i][1]]+= int(record_list2[i][3])
    else:
        differential = int(record_list2[i][3]) - int(record_list2[i][4])
        opponent[record_list2[i][1]][0]+=differential
        opponent[record_list2[i][1]][1]+=1
        # differential2 = int(record_list2[i][3]) - int(record_list2[i][4])
        # if differential2 > opponent[record_list2[i][1]]:
        #     opponent[record_list2[i][1]]=differential2

print(opponent)
listy2 =[]
for each in opponent.keys():
    list1 =[]
    if opponent[each][1] > 2:
        avg_da = opponent[each][0]/opponent[each][1]
        list1 =[avg_da, each]
        listy2.append(list1)
print(listy2)
# # Using min() + list comprehension + values()
# # Finding min value keys in dictionary
temp = max(opponent.values())
res = [key for key in opponent if opponent[key] == temp]
# print(res)
# gtech_score_list = [int(i[3]) for i in record_list2]
# # print(gtech_score_list)
# max1 = min(gtech_score_list)
# # print(min)
# index1= gtech_score_list.index(max1)
# # print(record_list2[index1][1])
# sec_list = list(range(1933, 1963+1))
# # print(sec_list)
# scored = [0, 0, 0]
# for i in range(0, len(record_list2)):
#     if int(record_list2[i][3]) == 0:
#         print(record_list2[i][1])
# #     #print(record_list2[i][0].year)
# #     if int(record_list2[i][0].year) in sec_list:
# #         if int(record_list2[i][3]) > int(record_list2[i][4]):
# #             scored[0]+=1
# #         elif int(record_list2[i][3]) < int(record_list2[i][4]):
# #             scored[1]+=1
# #         else:
# #             scored[2]+=1
# # # print(scored)

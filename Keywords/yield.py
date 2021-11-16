# #%% yield
#
#
# def squre():
#     i = 1
#     while True:
#         yield i+1
#         i +=1
#
# for each in squre():
#     if each > 10:
#         break
#     print(each)

a_list = (x for x in [1,2,3,4,5])
# print(a_list)
for each in a_list:
    print(each)


#"C:\Users\Admin\Desktop\mega.csv"
file1 = r"C:\Users\Admin\Desktop\mega.csv"
file_2 = r"C:\Users\Admin\Desktop\notmega.csv"
data = open(file1 , "r")
data1 = open(file_2, "r")
mega = data.read().splitlines()[1:]
not_mega = data1.read().splitlines()[1:]
print(not_mega)
# print(mega)
mega_list =[]
for each in mega:
    list1 = each.split(",")
    mega_list.append(list1)
# print(mega_list)
mega_list_nu = [i[0] for i in mega_list]
# print(mega_list_nu)

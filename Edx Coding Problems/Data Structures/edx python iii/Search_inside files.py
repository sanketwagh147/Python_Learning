a = open("sample.cs1301", mode="w")
a_list=["bhendi\n","gawar"]
content = a.writelines(a_list)
print(a)
a.close()
# >>['kanda\n', 'batata\n', 'tamata\n', 'wangi\n']
b = a = open("sample.cs1301", mode="r")
a_string = b.readlines()
print(a_string)

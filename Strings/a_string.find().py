"""Find the sub string in a string and returns its index else returns -1"""
data = "iam sanket and I am going to use find the sub-string in string variable called data"
sub_string = "sanket"
index_of_sub_string = data.find(sub_string, 0, 10)
print(index_of_sub_string)
#op: 42 ---the index location of s from sub-string
# index = data.index(sub_string)
# print(index)
print(data[43:])

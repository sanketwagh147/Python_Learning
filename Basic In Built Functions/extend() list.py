first_list = [1, 3, 4, 6]
second_list = ["kanda", "batata"]
first_list.append(second_list)
print(first_list)
print(second_list)
#  >>[[1, 3, 4, 6, ['kanda', 'batata']] # second list gets added as the
#      next item on the first list
#    ['kanda', 'batata'] # second list is not modified atall

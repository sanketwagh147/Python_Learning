# any will return false if the argument is only one of the following in the list below
false_list = ["", 0, 0.0, [], (), {}, False, None, 0j]
print(any(false_list))

#returns True if any one single value is True.
true_list = [{}, 1]
print(any(true_list))

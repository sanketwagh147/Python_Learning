#%% Type testing
a_list = [1, 2, 4]
if type(a_list) == type([]):
    print(True)
# using type name
if type(a_list) == list:
    print(True)
# object oriented test
if isinstance(a_list, list):
    print(True)

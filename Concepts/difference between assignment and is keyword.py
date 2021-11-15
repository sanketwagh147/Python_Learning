#%% use of assignment operator checks values
a_int = 1
b_int = 0
using_assignmet_true = a_int == True
using_assignmet_false = b_int == False
print(using_assignmet_false)
print(using_assignmet_true)
"""op:
True
True
"""
#%%% using equality i.e is keyword
"""the comparison also checks if the objects are of same type"""
a_int = 1
b_int = 0
using_assignmet_true = a_int is True
using_assignmet_false = b_int is False
print(using_assignmet_false)
print(using_assignmet_true)
"""op:
False
False
"""

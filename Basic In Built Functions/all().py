"""This function returns True if all the items in an iterable are true"""
#%%
egg = True
milk = True
butter = True
flour = True

a_list = [egg, milk, butter, flour]
print(all(a_list))
#%%
"""if a single object is false it returns False"""
egg = True
milk = True
butter = True
flour = False
a_list = [egg, milk, butter, flour]
print(all(a_list))

#%%
a = "race car"
a= a.replace("race", "dump")
print(a)
#%%
a_string = "replace all of idiots in the room with smart people of this company"
b_string = a_string.replace("of" # first parameter which will be replaced
, "the"  # Second parameter this is replaced in place of "of"
                 ,1)  # This is the third parameter which defined no of times replacing happens
print(b_string)

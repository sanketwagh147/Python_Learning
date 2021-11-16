#%%
"""even if string and list have same items if they don't have same order they wont return True
but if we convert them to set they will return True
we can also use sorted method to check string or list equality"""
a = 'spam' == 'asmp', set('spam') == set('asmp'), sorted('spam') == sorted('asmp')
print(a)
#op: (False, True, True)

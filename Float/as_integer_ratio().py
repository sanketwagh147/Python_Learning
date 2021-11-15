#%%
"""
as_integer_ration() is a method which converts a float value into fraction
of tuple type
"""
a_float = 2.5
b = a_float.as_integer_ratio()
print(b)
print(type(b))
#op: (5, 2)
#op: <class 'tuple'>

#%%
from fractions import Fraction
a_float = 2.5

"""
Fraction from float
"""
fraction_from_float = Fraction(*a_float.as_integer_ratio())  #(the * in the second test is special syntax that expands a tuple into individual arguments;

print(fraction_from_float)
print(type(fraction_from_float))
"""op: 
5/2
<class 'fractions.Fraction'>
"""

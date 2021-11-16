"""Convert into fraction taking input a float"""
from fractions import Fraction
a_float = 4.5
a_fraction = Fraction.from_float(a_float)
print(a_fraction)
print(type(a_fraction))
"""op:
9/2
<class 'fractions.Fraction'>
"""





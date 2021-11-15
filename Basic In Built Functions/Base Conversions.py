"""Convert the base from decimal to any other base
we cannot convert it from other to other only decimal to other"""
a_integer = 16
a_integer_binary = bin(a_integer)
a_integer_octal = oct(a_integer)
a_integer_hex = hex(a_integer)
print(a_integer_binary)
print(a_integer_octal)
print(a_integer_hex)
"""OP:
0b10000
0o20
0x10
"""

#%%
""" To use int() to convert the octal, decimal or hex in string form to integer"""
a_string_a ="10"
a_string_b ="40"
a_string_c ="FF"
a_integer_binary = int(a_string_a, 2)  # converts binary  "10" to decimal
a_integer_octal = int(a_string_b, 8)  # convert octal "40" string to decimal int form
a_integer_hex = int(a_string_c, 16)  # convert hex "FF" to decimal int form
print(a_integer_binary)
print(a_integer_octal)
print(a_integer_hex)

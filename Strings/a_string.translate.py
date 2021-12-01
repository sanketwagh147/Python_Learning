a_string = "Good night sam"
translate_ord_dict = {109: 65}

print(a_string.translate(translate_ord_dict))
print(chr(109), chr(65))

# * >> Good night saA
# value with  chr(109) is replaced by chr(65)

# Example 2:
# 
b_string = "Team'"
a_dict = {84: 109,
          101: 109,
          97: 109,
          109: 84 } 

# print(ord("T"), ord("e"), ord("a"), ord("m"))
print(b_string.translate(a_dict))
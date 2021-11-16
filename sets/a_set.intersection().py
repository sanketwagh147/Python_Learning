""""acts as intersection & does the same"""
a_set = set("spam")
print(a_set)
c_set = a_set.intersection(set("eggs"))
print(c_set)
"""op: 
{'s', 'a', 'm', 'p'}
{'s'}
"""

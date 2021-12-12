"""adds to a set """
a_set = set("spam")
print(a_set)
a_set.add("eggs")
print(a_set)
"""op: 
{'s', 'a', 'm', 'p'} 
{'s', 'm', 'eggs', 'a', 'p'}
"""


# use case

list_ = [1 ,2, 1, 2, 3, 4]
is_in = set()
for each in list_:
    if each not in is_in:
        is_in.add(each)
    

print(list(is_in))

string = "ab"
stringb = "ca"
print(string + stringb)

        
print("ab".join("ca")        )

"""create a set using {} """
a_set = {"s", "p", "a", "m"}
print(a_set)
print(type(a_set))
"""op:
{'s', 'a', 'm', 'p'}
<class 'set'>
"""
#%%
"""create a set using set() """
a_set = set("eggs")
print(a_set)
#op: {'e', 'g', 's'}

#%%
"""sets can only contain immutable or hashable object types ,
 list and dictionaries cannot be implemented in sets"""
a_set = {1,2, "string", 3.5, ["list",11,22]} # sets cannot contain mutable type
"""
Traceback (most recent call last):
  File "<input>", line 3, in <module>
TypeError: un hashable type: 'list'"""
#%%

a_set = set("spam")
print(a_set)
a_set.add("d")
print(a_set)

#%%% Frozen set
a_set = frozenset("spam")
print(a_set)
print(type(a_set))

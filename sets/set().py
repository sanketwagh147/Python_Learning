#%%
from icecream import ic
set1 = set("spam")
set11 = list(set("spam"))
ic(set1)
set2 = set("pam")
set22 = list(set("pam"))
ic(set2)
intersection = set1 & set2
ic(intersection)
union = set1 | set2
ic(union)
difference = set1 - set2
ic(difference)
ic(set1 > set2)  # check if set1 is superset of set2
ic(set2 < set1)  # check if set2 is subset of set1

#OP:
# ic| set1: {'m', 's', 'p', 'a'}
# ic| set2: {'m', 'p', 'a'}
# ic| intersection: {'m', 'p', 'a'}
# ic| union: {'s', 'p', 'm', 'a'}
# ic| difference: {'s'}
# ic| set1 > set2: True
# ic| set2 < set1: True

#%% set ird

"""It is similar to slice[start:end:step]
except it is a function and uses , as a separator"""
listy = list(range(0,10))
sliced = listy[slice(2,8,2)]
print(sliced)

import shelve
db = shelve.open("persondb")
len(db)
list(db.keys())
print(len(db))

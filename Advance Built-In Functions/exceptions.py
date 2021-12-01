

# ? Case I 
try:
    # a = 3
    print(a)
    
except NameError as name:
    print(name)  # exception inside

# * Prints the error message >> name 'a' is not defined

# ? Case II
try:
    # a = 3
    print(a)
    
except NameError as name:
    print({"------------"})

print(name)  # ! error is availabe only locally


# ? Case III save the error to another variable

try:
    # a = 3
    print(a)
    
except NameError as name:
    save_error = name  # * save error for further referencing
    print({"------------"})

print(save_error)   # Error is now availabe for further referencing
# join using string
separator_string = "@"
list1 = ["sanketwagh147", "gmail.com"]
join_using_separator = separator_string.join(list1)
print(join_using_separator)
# >>>sanketwagh147@gmail.com

# We can also use a string directly instead of a variable string as separator string
join_using_separator_2 = "\u263a".join(list1)
print(join_using_separator_2)
# >>>sanketwagh147☺gmail.com


kanda = "waka".join([" boka ", "boka ", "boka ", "boka ", "boka" , "boka"])
print(kanda)

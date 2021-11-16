# To find the max number
a_list = list(range(0, 10, 2))
print(a_list)
print(max(a_list))

# To find the max string based on first character of string and ordinal number
languages = ["Python", "C Programming", "Java", "JavaScript"]
largest_string = max(languages)
print(largest_string)
ordinal_list = [ord(i[0]) for i in languages]
print(ordinal_list)

#to find max between two or more arguments using key
print(max("sukanya", "sanket","wagh" , key=len))

#Write a function called imdb_dictionary. imdb_dictionary
#should have one parameter, a string representing a
#filename.
#
#On each row of the file will be a performer's name, then
#a semicolon, then a comma-separated list of movies the have
#been in. For example, one file's contents could be:
#
#Robert Downey Jr.; Avengers: Infinity War, Sherlock Holmes 3, Spider-Man: Homecoming
#Scarlett Johansson; Avengers: Infinity War, Isle of Dogs, Ghost in the Shell
#Elizabeth Olsen; Avengers: Infinity War, Kodachrome, Wind River, Ingrid Goes West
#
#You may assume that the only semi-colon will be after the
#performer's name, and that there will be no commas in the
#movie titles.
#
#Return a dictionary where the keys are each actor's name,
#and the values are alphabetically-sorted lists of the movies
#they have been in. For example, if imdb_dictionary was called
#on the file above, the output would be:
#{"Robert Downey Jr.": ["Avengers: Infinity War", "Sherlock Holmes 3", "Spider-Man: Homecoming"],
#"Scarlett Johansson": ["Avengers: Infinity War", "Ghost in the Shell", "Isle of Dogs"],
#Elizabeth Olsen": ["Avengers: Infinity War", "Ingrid Goes West", "Kodachrome", "Wind River"]}
#
#Make sure the list of movies is sorted alphabetically. Don't
#worry about the order the keys (names) appear in the dictionary.


#Add your code here!
def imdb_dictionary(a_string):
    a_file = open(a_string, "r")
    contents = a_file.read()
    # print(contents)
    list1 = contents.splitlines()
    # print(list1)
    a_file.close()
    return_dict = {}
    for each in range(0, len(list1)):
        # print(list1[each])
        # print(type(list1[each]))
        list2 = list1[each].split(";")
        # print(list2)
        list2[1].split(",").sort()
        # print(list2)
        list2[1].split(",").sort()
        star_name = list2[0].strip()
        list2.pop(0)
        # print(list2)
        list3 = list2[0].split(",")
        list3.sort()
        list4 = []
        for element in list3:
            list4.append(element.strip())
        return_dict[star_name] = list4
    # print(return_dict)
    return return_dict


#Below are some lines of code that will test your function.
#You can change the contents of some_performers.txt from
#the dropdown in the top left to test other inputs.
#
#If your function works correctly, this will originally
#print (although the order of the keys may vary):
#{"Robert Downey Jr.": ["Avengers: Infinity War", "Sherlock Holmes 3", "Spider-Man: Homecoming"], "Scarlett Johansson": ["Avengers: Infinity War", "Ghost in the Shell", "Isle of Dogs"], Elizabeth Olsen": ["Avengers: Infinity War", "Ingrid Goes West", "Kodachrome", "Wind River"]}
print(imdb_dictionary("some_performers.txt"))





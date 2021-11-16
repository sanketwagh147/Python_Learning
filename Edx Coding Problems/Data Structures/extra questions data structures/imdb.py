#Write a function called imdb_dictionary. imdb_dictionary
#should have one parameter, a string representing a
#filename.
#
#On each row of the file will be a comma-and-space-separated
#list of movies, then a colon, then a performer's name. For
#example, one file's contents could be:
#
#Avengers: Infinity War, Sherlock Holmes 3, Spider-Man: Homecoming; Robert Downey Jr.
#Avengers: Infinity War, Isle of Dogs, Ghost in the Shell; Scarlett Johansson
#Avengers: Infinity War, Kodachrome, Wind River, Ingrid Goes West; Elizabeth Olsen
#
#You may assume that the only semi-colon will be before the
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
#
#Hint: Remember to deal with the spaces after the commas and
#semicolons!


#Add your code here!
def imdb_dictionary(a_string):
    a_file = open(a_string, "r")
    contents = a_file.read()
    # print(contents)
    list1 = contents.splitlines()
    # print(list1)
    a_file.close()
    return_dict = {}
    for each_item in list1:
        # print(each_item)
        list2 = each_item.split(";")
        # print(list2)
        star_name = list2.pop().lstrip()
        # print(star_name)
        # print(list2)
        movie_list = list2[0].split(",")
        # print(movie_list)
        movie_list2 = []
        for each_item2 in movie_list:
            # print(each_item2)
            movie_list2.append(each_item2.strip())
        movie_list2.sort()
        # print(movie_list2)
        return_dict[star_name] = movie_list2
    return return_dict
#Below are some lines of code that will test your function.
#You can change the contents of some_performers.txt from
#the dropdown in the top left to test other inputs.
#
#If your function works correctly, this will originally
#print (although the order of the keys may vary):
#{"Robert Downey Jr.": ["Avengers: Infinity War", "Sherlock Holmes 3", "Spider-Man: Homecoming"], "Scarlett Johansson": ["Avengers: Infinity War", "Ghost in the Shell", "Isle of Dogs"], Elizabeth Olsen": ["Avengers: Infinity War", "Ingrid Goes West", "Kodachrome", "Wind River"]}
print(imdb_dictionary("some_performers.txt"))






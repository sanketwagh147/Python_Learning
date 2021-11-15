#This is a challenging one! The output will be very long as
#you'll be working on some pretty big dictionaries. We don't
#expect everyone to be able to do it, but it's a good chance
#to test how far you've come!
#
#Write a function called stars that takes in two
#dictionaries:
#
# - movies: a dictionary where the keys are movie titles and
#   the values are lists of major performers in the movie. For
#   example: movies["The Dark Knight"] = ["Christian Bale",
#   "Heath Ledger", "Maggie Gyllenhall", "Aaron Eckhart"]
# - tvshows: a dictionary where the keys are TV show titles
#   and the values lists of major performers in the show.
#   For example: tvshows["Community"] = ["Joel McHale", "Alison
#   Brie", "Danny Pudi", "Donald Glover", "Yvette Brown"]
#
#The function stars should return a new dictionary. The keys
#of the new dictionary should be the performers' names, and
#the values for each key should be the list of shows and
#movies in which that performer has appeared. Sort the shows
#and movies alphabetically.


#Write your function here!
def stars(movies, tv_shows):
    dictionary_to_return = {}
    for k, v in {**movies, **tv_shows}.items():
        for actor in v:
            dictionary_to_return.setdefault(actor, []).append(k)

    dictionary_to_return = {k: sorted(v) for k,v in dictionary_to_return.items()}  #Sort by show-movie
    return dictionary_to_return


# def stars(movies, tv_shows):
#     # print(movies)
#     # print(tv_shows)
#     dictionary_to_return = {}
#     both_dict = {**movies, **tv_shows}
#     # print(both_dict)
#     celebrity_list = []
#     # # print(celebrity_list)
#     for (key, value) in both_dict.items():
#         celebrity_list.extend(value)
#         celebrity_list_filtered = list(set(celebrity_list))
#     celebrity_list_filtered.sort()
#     # print(celebrity_list_filtered)
#     for every_celebrity in celebrity_list_filtered:
#         # print(every_celebrity,": THis is artist")
#         for every_title in both_dict.keys():
#             # print(every_title,": THis is the tile")
#             artist_in_title = both_dict[every_title]
#             # print(artist_in_title, ":these are artist in the", every_title)
#             if every_celebrity in artist_in_title:
#                 if every_title not in dictionary_to_return.keys():
#                     celebrity_list.append(every_title)
#
#                 else:
#                     valuess = dictionary_to_return[every_celebrity].value
#                     print(valuess)
#                 print(celebrity_list)
#     print(dictionary_to_return)
                # print(type(artist_in_title))
                # (every_celebrity,)
    # ret_list =[]
    # individual_tilte_list=[]
    # ret_dict ={}
    # for every_celebrity in celebrity_list_filtered:
    #     # print(every_celebrity)
    #     for (each_title,value) in both_dict.items():
    #         if every_celebrity in both_dict[each_title]:
    #             ret_list.append(every_celebrity)
    #             ret_list.append(key)
    # print(ret_list)
    # for i in range(0, len(ret_list)):
    #     if ret_list[i] in celebrity_list_filtered:
    #         if ret_list[i] in individual_tilte_list:
    #             individual_tilte_list.append(ret_list[0+i])
    #     elif ret_list[i] not in celebrity_list_filtered:
    #         individual_tilte_list.append(ret_list[i])
    # print(individual_tilte_list)

    #


#Below are some lines of code that will test your function.
#You can change the value of the variable(s) to test your
#function with different inputs.
#
#If your function works correctly, this will originally
#print (although the order of the keys may vary):
#
#{'Portia de Rossi': ['Arrested Development'], 'Will Ferrell': ['The Lego Movie'], 'Yvette Brown': ['Community'], 'Rebel Wilson': ['How to Be Single'], 'Danny Pudi': ['Community'], 'Elizabeth Banks': ['30 Rock', 'The Lego Movie'], 'Alec Baldwin': ['30 Rock'], 'Alison Brie': ['Community', 'How to Be Single', 'The Lego Movie'], 'Tina Fey': ['30 Rock'], 'Dakota Johnson': ['How to Be Single'], 'Joel McHale': ['Community'], 'Jack McBrayer': ['30 Rock'], 'Tracy Morgan': ['30 Rock'], 'Donald Glover': ['Community'], 'Will Arnett': ['Arrested Development', 'The Lego Movie'], 'Jason Bateman': ['Arrested Development']}
#
movies = {"How to Be Single": ["Alison Brie", "Dakota Johnson",
                               "Rebel Wilson"],
          "The Lego Movie": ["Will Arnett", "Elizabeth Banks",
                             "Alison Brie", "Will Ferrell"]}
tvshows = {"Community": ["Alison Brie", "Joel McHale",
                         "Danny Pudi", "Yvette Brown",
                         "Donald Glover"],
           "30 Rock": ["Tina Fey", "Tracy Morgan", "Jack McBrayer",
                       "Alec Baldwin", "Elizabeth Banks"],
           "Arrested Development": ["Jason Bateman", "Will Arnett",
                                    "Portia de Rossi"]}
print(stars(movies, tvshows))


# movies = {"lavda": ["L", "A",
#                                "D"],
#           "lasun": ["L", "A",
#                              "S", "U"]}
# tvshows = {"Lambda": ["L", "A",
#                          "M", "D",
#                          "A"],
#            "kutta": ["K", "U", "T",
#                        "A", "X"],
#            "chutiya": ["C", "H",
#                                     "U"]}
# print(stars(movies, tvshows))
#
#sample 1

#This is a complex one, but when you break it down into
#smaller parts, it becomes a lot easier to follow!

def stars(movies, tvshows):

    #First, as usual: our goal is to create a new
    #dictionary, so we start my initializing a new
    #dictionary:

    new_dict = {}

    #Now, we want to separately go through the
    #movies and tvshows dictionaries. Let's start with
    #movies.
    #
    #We're going to iterate through every
    #movie-performers pair in the dictionary:

    for movie, performers in movies.items():

        #Now, movie is a string, and performers is a
        #list of strings. The strings in performers
        #are people: that's what we want the keys to
        #our new dictionary to be. So, we iterate
        #through each performer in this movie's list
        #of performers:

        for performer in performers:

            #Now, performer is the name of one person.
            #We want that person to be in new_dict as
            #a key, with a list of their movies and
            #TV shows as the value.
            #
            #If they're already in new_dict, we just
            #want to add this movie to their list.
            #But first, we should check to see if
            #they're already in new_dict: if they
            #aren't, then there's no list to add to!

            if performer not in new_dict:

                #If they aren't, then we should create
                #a new key with this performer's name,
                #and give it an empty list as its value:

                new_dict[performer] = []

            #Here, we can guarantee that performer is now
            #a key in new_dict: if it wasn't before, we
            #just added it! So, we can now add movie to
            #the list.
            #
            #We access the list with new_dict[performer],
            #and we can then call append(movie) directly:

            new_dict[performer].append(movie)

            #And that's all! We've now added movie to this
            #performer's value in new_dict. If this
            #performer wasn't already in new_dict, we added
            #them first.

    #Next, we do the *exact* same thing for tvshows. In fact,
    #it's identical: the code below is copy/pasted from above,
    #but with tvshow used instead of movie. So, it works
    #identically:
    for tvshow, performers in tvshows.items():
        for performer in performers:
            if performer not in new_dict:
                new_dict[performer] = []
            new_dict[performer].append(tvshow)

    #Now, recall that we have to sort the names of each
    #performer's movies and TV shows alphabetically. How do
    #we do that? We could have re-sorted them each time we
    #appended a new movie or TV show, but that would be
    #inefficient: we'd sort a lot more often than we need to.
    #Instead, let's go through all the performers at the end
    #and sort their lists.
    #
    #So, we iterate through each performer-performances pair
    #in new_dict:

    for performer, performances in new_dict.items():

        #And sort the performances. Remember, lists are
        #mutable, so any methods we run on them like
        #performances.sort() change them in place: we don't
        #need to set performances equal to the sorted version
        #of itself.

        performances.sort()

    #Now we're done!

    return new_dict

    #Notice, though, that the TV shows code was identical to
    #the movies code. That's generally undesirable. What if
    #we made a mistake? We'd have to fix it in two places.
    #Instead, we should encapsulate that reasoning in a
    #separate function that we can call separately on movies
    #and TV shows. Check out sample_answer_2.py for that.






movies = {"How to Be Single": ["Alison Brie", "Dakota Johnson",
                               "Rebel Wilson"],
          "The Lego Movie": ["Will Arnett", "Elizabeth Banks",
                             "Alison Brie", "Will Ferrell"]}
tvshows = {"Community": ["Alison Brie", "Joel McHale",
                         "Danny Pudi", "Yvette Brown",
                         "Donald Glover"],
           "30 Rock": ["Tina Fey", "Tracy Morgan", "Jack McBrayer",
                       "Alec Baldwin", "Elizabeth Banks"],
           "Arrested Development": ["Jason Bateman", "Will Arnett",
                                    "Portia de Rossi"]}
print(stars(movies, tvshows))



#sample 2

#Our reasoning here will be largely the same, but we
#want to create a separate function to handle
#transforming movie-performers dictionaries into a
#performer-performances dictionary.
#
#So, let's first write a general function that does
#that. It will take two parameters: the original
#dictionary (something like movies or tvshows, which
#maps performance names to lists of performers) and
#the new dictionary (which maps performer names to
#lists of performances):

def movies_to_performers(orig_dict, new_dict):
    for performance, performers in orig_dict.items():
        for performer in performers:
            if performer not in new_dict:
                new_dict[performer] = []
            new_dict[performer].append(performance)

#Compare this to the reasoning in sample_answer_1.py.
#You'll see it's *identical*: all we did was replace
#movies or tvshows with orig_dict, and movie or tvshow
#with performance.
#
#What good does that do us? Check out how simple our
#stars() function is now:

def stars(movies, tvshows):
    new_dict = {}
    movies_to_performers(movies, new_dict)
    movies_to_performers(tvshows, new_dict)

    for performer, performances in new_dict.items():
        performances.sort()
    return new_dict

    #By using a function like movies_to_performers, we let
    #ourselves call that long block of code multiple times
    #in only one line of code each.


movies = {"How to Be Single": ["Alison Brie", "Dakota Johnson",
                               "Rebel Wilson"],
          "The Lego Movie": ["Will Arnett", "Elizabeth Banks",
                             "Alison Brie", "Will Ferrell"]}
tvshows = {"Community": ["Alison Brie", "Joel McHale",
                         "Danny Pudi", "Yvette Brown",
                         "Donald Glover"],
           "30 Rock": ["Tina Fey", "Tracy Morgan", "Jack McBrayer",
                       "Alec Baldwin", "Elizabeth Banks"],
           "Arrested Development": ["Jason Bateman", "Will Arnett",
                                    "Portia de Rossi"]}
print(stars(movies, tvshows))




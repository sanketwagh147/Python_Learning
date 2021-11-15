import ast
movie_list = []
input_file = open("movies.txt", "r")
for line in input_file:
    line_as_tuple = ast.literal_eval(line)
    movie_list.append(line_as_tuple)
input_file.close()
print(movie_list)

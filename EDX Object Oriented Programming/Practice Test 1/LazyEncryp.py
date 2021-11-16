#Write a function called lazy_encrypt. This function should
#take three parameters: two strings and a dictionary. The
#first string is the filename of a file to which to write
#(output_file), the second string is the filename of a file
#from which to read (input_file), and the dictionary is a
#mapping of character:character pairs you should use to
#"encrypt" the contents of the input file before writing it
#to the output file.
#
#lazy_encrypt should go through every character in the
#input file. If the character is a key in the dictionary,
#then lazy_encrypt should write the value associated with
#that key to the output file. If it is not a key, it should
#write the original character.
#
#For example, imagine if the input file contained the text
#"Hello world", and the dictionary was {"e": "o", "o": "a"}.
#Then, lazy_encrypt would write "Holla warld" to the output
#file. Each letter is only substituted once. You should not
#ignore case: if the input file had instead contained the
#text "HELLO WORLD", then nothing should have been changed
#because the keys in the dictionary are lower-case.
#
#We've included two files for you to test on: anInputFile.txt
#and anOutputFile.txt. The test code below will copy the text
#from the first file to the second. Feel free to modify the
#first to test different setups.


#Write your function here!
def lazy_encrypt(file_out, file_in, a_dict):
    data_in = open(file_in, "r")
    data_str = data_in.read()
    data_out = open(file_out,"w")
    write_string=""
    for each in data_str:
        if each in a_dict.keys():
            write_string += a_dict[each]
        else:
            write_string += each
    data_out.write(write_string)


#The code below will test your function. You can find the two
#files it references in the drop-down in the top left. If your
#code works, the contents of anOutputFile.txt after running
#will be:
#Horo is a protty simplo mossago ta oncrypt
#Whon it's oncryptod, it will laak difforont

lazy_encrypt("anOutputFile.txt", "anInputFile.txt", {"e": "o", "o": "a"})
print("Done running! Check anOutputFile.txt for the result.")


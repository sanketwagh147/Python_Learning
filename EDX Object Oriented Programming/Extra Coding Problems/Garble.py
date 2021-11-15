#Write a function called garble_this. This function should
#take two parameters, both strings. The first string is the
#filename of a file to which to write (output_file), and the
#second string is the filename of a file from which to read
#(input_file).
#
#garble_this should copy the contents of input_file into
#output_file, but make the following changes:
#
# - Replace all vowels with the next vowel in order (a -> e,
#   e -> i, i -> o, o -> u.
# - Replace all consonants with the next consonant, b -> c,
#   c -> d, d -> f, etc.) Replace z with b.
# - Leave everything else in the file unchanged.
#
#For example, if these were the contents of input_file (the
#second parameter):
#
# this is some text. woo text yay!
#
#Then garble_this would write this text to output_file (the
#first parameter):
#
# vjot ot tuni viyv. xuu viyv zez!
#
#No other characters should be changed. Note that the file
#to be copied will have multiple lines of text. You may assume
#the input file will be all lower-case.
#
#We've included two files for you to test on: anInputFile.txt
#and anOutputFile.txt. The test code below will copy the text
#from the first file to the second. Feel free to modify the
#first to test different setups.
#
#Hints:
# - Remember, you can increment a letter by 1 by finding its
#   ordinal, adding one, and converting it back to a letter.
#   If a_char is a character, then chr(ord(a_char) + 1) would
#   give you the next character.
# - You might also use dictionaries to establish what each
#   letter gets replaced by.
# - In ASCII, the character that comes after "z" is "{". You
#   want to replace "z" with "a", though.
# - Consider writing multiple functions! You could (but you
#   do not have to) write a dedicated function called
#   change_letter that handles a single letter, then
#   repeatedly call it to handle the file as a whole.
# print(ord("a"))
from icecream import icecream as ic
#Write your function here!
def garble_this(out_file, inp_file):
    file_in = open(inp_file, "r")
    file_out = open(out_file, "w")
    data_in = file_in.read()
    data_out = ""
    vowel_list = [ord("a"), ord("e"), ord("i"), ord("o"), ord("u")]
    small_alphabets_ord = list(range(97,123))
    consonant_list = list(set(vowel_list) ^ set(small_alphabets_ord))
    print(consonant_list)
    for i in range(0, len(data_in)):
        print(chr(ord(data_in[i])))
        if ord(data_in[i]) in vowel_list:
            # print(chr(ord(data_in[i])))
            if ord(data_in[i]) == ord("u"):
                data_out += chr(ord("a"))
            else:
                # print("ord(data_in[i])", ord(data_in[i]))
                vowel = vowel_list.index(ord(data_in[i]))
                # print("vowel", vowel)
                data_out += chr(vowel_list[vowel+1])
                # print(data_out)
        elif ord(data_in[i]) in consonant_list:
            if ord(data_in[i]) == ord("z"):
                data_out += "a"
            else:
                cons = consonant_list.index(ord(data_in[i]))
                print("cons", cons)
                data_out += chr(consonant_list[cons+1])
                print(chr(consonant_list[cons+1]))
        else:
            data_out += data_in[i]
    file_out.write(data_out)
    file_in.close()
    file_out.close()




#The code below will test your function. You can find the two
#files it references in the drop-down in the top left. If your
#code works, anOutputFile.txt should have the text:
#ecdfigh
#joklmnp
#uqrstva
#wxyzb.!
#1234567
#890&$%#

garble_this("anOutputFile.txt", r"C:\Users\Admin\PycharmProjects\Practice\Object Oriented Programming EDX\Extra Coding Problems\anInputFile1.txt")
print("Done running! Check anOutputFile.txt for the result.")


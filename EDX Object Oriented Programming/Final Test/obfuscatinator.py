#Write a function called deobfuscate. This function should
#take two parameters, both strings. The first string is the
#filename of a file to which to write (output_file), and the
#second string is the filename of a file from which to read
#(input_file).
#
#deobfuscate should copy the contents of input_file into
#output_file, with one twist: every pair of characters should
#be swapped. So, if the original file contained the text:
#
# BADCFEG
#
#Then the output file would contain the text ABCDEFG: the
#B and A swap; the D and C swap; and the F and E swap. The
#G is left alone; if there are an odd number of characters,
#leave the final character alone.
#
#This change should be applied to every character in the
#file: punctuation, spaces, and even line breaks. So, if the
#original file was:
#
# abc def
# ghi jkl
#
#Then the output file would contain:
#
# ba ced
# fhg ikjl
#
#Note that the c and space switch places, and that the f
#switches places with the line break immediately after it,
#which bumps the f down to the next line.
#
#We've included two files for you to test on: anInputFile.txt
#and anOutputFile.txt. The test code below will copy the text
#from the first file to the second. Feel free to modify the
#first to test different setups.


#Write your function here!
def deobfuscate(out_file, in_file):
    data_in = open(in_file, "r")
    data_out = open(out_file, "w")
    data_read = data_in.read()
    data_write =""
    list1 = list(range(0, len(data_read)))
    # print(list1)
    # print(len(data_read))
    # if len(data_read) % 2 == 1:
    #     data_read = data_read[:-1]
        # print(data_read)
    # print(data_read)
    split_string = [data_read[i:i+2] for i in range(0, len(data_read), 2)]
    print(split_string)
    for each in split_string:
        print(each)
        if len(each)==1:
            data_write += each[0]
        else:
            data_write += each[1]
            data_write += each[0]
    # print(len(data_read))
    # for each in list1:
    #     if each % 2 == 0:
    #         data_write += data_read[each]
    #         data_write += data_read[each-1]
    data_out.write(data_write)
    #
    #


#The code below will test your function. You can find the two
#files it references in the drop-down in the top left. If your
#code works, anOutputFile.txt should have the text:
#I'm a Ramblin' Wreck
#from Georgia Tech
deobfuscate("anOutputFile.txt", "anInputFile.txt")
print("Done running! Check anOutputFile.txt for the result.")


#If you accidentally erase anInputFile.txt, here's its original
#text to copy back in:
#'I m aaRbmil'nW erkcf
#or meGroig aeThc

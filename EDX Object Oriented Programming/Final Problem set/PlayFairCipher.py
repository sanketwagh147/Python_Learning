# #One of the early common methods for encrypting text was the
# #Playfair cipher. You can read more about the Playfair cipher
# #here: https://en.wikipedia.org/wiki/Playfair_cipher
# #
# #The Playfair cipher starts with a 5x5 matrix of letters,
# #such as this one:
# #
# # D A V I O
# # Y N E R B
# # C F G H K
# # L M P Q S
# # T U W X Z
# #
# #To fit the 26-letter alphabet into 25 letters, I and J are
# #merged into one letter. When decrypting the message, it's
# #relatively easy to tell from context whether a letter is
# #meant to be an i or a j.
# #
# #To encrypt a message, we first remove all non-letters and
# #convert the entire message to the same case. Then, we break
# #the message into pairs. For example, imagine we wanted to
# #encrypt the message "PS. Hello, worlds". First, we could
# #convert it to PSHELLOWORLDS, and then break it into letter
# #pairs: PS HE LL OW OR LD S. If there is an odd number of
# #characters, we add X to the end.
# #
# #Then, for each pair of letters, we locate both letters in
# #the cipher square. There are four possible orientations
# #for the pair of letters: they could be in different rows
# #and columns (the "rectangle" case), they could be in the
# #same row but different columns (the "row" case), they could
# #be in the same column but different rows (the "column"
# #case), or they could be the same letter (the "same" case).
# #
# #Looking at the message PS HE LL OW OR LD SX:
# #
# # - PS is the Row case: P and S are in the same row.
# # - HE is the Rectangle case: H and E are in different rows
# #   and columns of the square.
# # - LD is the Column case: L and D are in the same column.
# # - LL is the Same case as it's two of the same letter.
# #
# #For the Same case, we replace the second letter in the pair
# #with X, and then proceed as normal. When decrypting, it
# #would be easy to see the our result was not intended to be
# #PS HELXO WORLDSX, and we would thus assume the X is meant to
# #repeat the previous letter, becoming PS HELLO WORLDSX.
# #
# #What we do for each of the other three cases is different:
# #
# # - For the Rectangle case, we replace each letter with
# #   the letter in the same row, but the other letter's
# #   column. For example, we would replace HE with GR:
# #   G is in the same row as H but the same column as E,
# #   and R is in the same row as E but the same column as
# #   H. For another example, CS would become KL: K is in
# #   C's row but S's column, and L is in C's column but S's
# #   row.
# # - For the Row case, we pick the letter to the right of
# #   each letter, wrapping around the end of the row if we
# #   need to. PS becomes QL: Q is to the right of P, and L
# #   is to the right of S if we wrap around the end of the
# #   row.
# # - For the Column case, we pick the letter below each
# #   letter, wrapping around if necessary. LD becomes TY:
# #   T is below L and Y is below D.
# #
# #We would then return the resultant encrypted message.
# #
# #Decrypting a message is essentially the same process.
# #You would use the exact same cipher and process, except
# #for the Row and Column cases, you would shift left and up
# #instead of right and down.
# #
# #Write two methods: encrypt and decrypt. encrypt should
# #take as input a string, and return an encrypted version
# #of it according to the rules above.
# #
# #To encrypt the string, you would:
# #
# # - Convert the string to uppercase.
# # - Replace all Js with Is.
# # - Remove all non-letter characters.
# # - Add an X to the end if the length if odd.
# # - Break the string into character pairs.
# # - Replace the second letter of any same-character
# #   pair with X (e.g. LL -> LX).
# # - Encrypt it.
# #
# #decrypt should, in turn, take as input a string and
# #return the unencrypted version, just undoing the last
# #step. You don't need to worry about Js and Is, duplicate
# #letters, or odd numbers of characters in decrypt.
# #
# #For example:
# #
# # encrypt("PS. Hello, world") -> "QLGRQTVZIBTYQZ"
# # decrypt("QLGRQTVZIBTYQZ") -> "PSHELXOWORLDSX"
# #
# #HINT: You might find it easier if you implement some
# #helper functions, like a find_letter function that
# #returns the row and column of a letter in the cipher.
# #
# #HINT 2: Once you've written encrypt, decrypt should
# #be trivial: try to think of how you can modify encrypt
# #to serve as decrypt.
# #
# #To make this easier, we've gone ahead and created the
# #cipher as a 2D tuple for you:
# CIPHER = (("D", "A", "V", "I", "O"),
#           ("Y", "N", "E", "R", "B"),
#           ("C", "F", "G", "H", "K"),
#           ("L", "M", "P", "Q", "S"),
#           ("T", "U", "W", "X", "Z"))
# # CIPHER = (("0", "1", "2", "3", "4", "C"),
# #           ("1", "D", "A", "V", "I", "O"),
# #           ("2", "Y", "N", "E", "R", "B"),
# #           ("3", "C", "F", "G", "H", "K"),
# #           ("4", "L", "M", "P", "Q", "S"),
# #           ("5", "T", "U", "W", "X", "Z"))
#
# # [([4, 3], [4, 5]), ([3, 4], [2, 3]), ([4, 1], [5, 4]), ([1, 5], [5, 3]), ([1, 5], [2, 4]), ([4, 1], [1, 1])]
# # [([3, 2], [3, 4]), ([2, 3], [1, 2]), ([3, 0], [4, 3]), ([0, 4], [4, 2]), ([0, 4], [1, 3]), ([3, 0], [0, 0])]
# #Add your code here!
# from icecream import ic
# def find_case(a_list):
#     if a_list[0] == a_list[2]:
#         # ic("row case")
#         return "ROW"
#     elif a_list[1] == a_list[3]:
#         # ic("column case")
#         return "COL"
#     else:
#         return "REC"
# def find_loc(a_str):
#     # ic(a_str[0],a_str[1])
#     for i in range(0, len(CIPHER)):
#         for j in range(0, len(CIPHER[i])):
#             # ic(CIPHER[i][j])
#             if a_str[0] == CIPHER[i][j]:
#                 loc0 = [i,j]
#             if a_str[1] == CIPHER[i][j]:
#                 loc1 = [i,j]
#     return loc0+loc1
# def encrypt(a_string):
#     ic(a_string)
#     upper = a_string.upper()
#     ic(upper)
#     filter_string = ''.join(char for char in upper if char.isalpha())
#     ic(filter_string)
#     replace_i = filter_string.replace("J", "I")
#     ic(replace_i)
#     if len(replace_i) % 2 == 1:
#         replace_i = replace_i+"X"
#     # split replace_i in 2 list
#     step = 2
#     split_strings = [replace_i[i: i + step] for i in range(0, len(replace_i), step)]
#     ic(split_strings)
#     for i in range(0, len(split_strings)):
#         if split_strings[i][0] == split_strings[i][1]:
#             split_strings[i] = str(split_strings[i][0])+"X"
#     ic(split_strings)
#     loc_list = []
#     for each_set in split_strings:
#         loc = find_loc(each_set)
#         loc_list.append(loc)
#     ic(loc_list)
#     case_list = []
#     for each in loc_list:
#         case = find_case(each)
#         case_list.append(case)
#     ic(case_list)
#     # for i in range(0, len(loc_list)):
#
# # def decrypt(a_string):
#
#
# #Below are some lines of code that will test your function.
# #You can change the value of the variable(s) to test your
# #function with different inputs.
# #
# #If your function works correctly, this will originally
# #print: QLGRQTVZIBTYQZ, then PSHELXOWORLDSX
# print(encrypt("PS. Hello, world"))
# # print(decrypt("QLGRQTVZIBTYQZ"))
# # ic(find_loc("HE"))
# Write two methods: encrypt and decrypt. encrypt should
# take as input a string, and return an encrypted version#of it according to the rules above.
#
#
# # Answer
#
# CIPHER = (("D", "A", "V", "I", "O"),
#
#          ("Y", "N", "E", "R", "B"),
#
#          ("C", "F", "G", "H", "K"),
#
#          ("L", "M", "P", "Q", "S"),
#
#          ("T", "U", "W", "X", "Z"))
#
# # Add your code here!
# import icecream as ic
# def encrypt(a_string):
#    a_list = []
#    for char in a_string:
#        if char.isalpha():
#            char = char.upper()
#            if char == "J":
#                char = "I"
#            a_list.append(char)
#    print(a_list)
#    if len(a_list) % 2 == 1:
#        a_list.append("X")
#    for i in range(0, len(a_list), 2):
#        if a_list[i] == a_list[i + 1]:
#            a_list[i + 1] = "X"
#        index1 = [-1, -1]
#        index2 = [-1, -1]
#        for j in range(len(CIPHER)):
#            for k in range(len(CIPHER)):
#                if a_list[i] == CIPHER[j][k]:
#                    index1 = [j, k]
#                if a_list[i + 1] == CIPHER[j][k]:
#                    index2 = [j, k]
#        if (index1[0] == index2[0]):
#            index1[1] += 1
#            index2[1] += 1
#            if index1[1] == 5:
#                index1[1] = 0
#            if index2[1] == 5:
#                index2[1] = 0
#            a_list[i] = CIPHER[index1[0]][index1[1]]
#            a_list[i + 1] = CIPHER[index2[0]][index2[1]]
#
#        elif (index1[1] == index2[1]):
#            index1[0] += 1
#            index2[0] += 1
#            if index1[0] == 5:
#                index1[0] = 0
#            if index2[0] == 5:
#                index2[0] = 0
#            a_list[i] = CIPHER[index1[0]][index1[1]]
#            a_list[i + 1] = CIPHER[index2[0]][index2[1]]
#        else:
#            a_list[i] = CIPHER[index1[0]][index2[1]]
#            a_list[i + 1] = CIPHER[index2[0]][index1[1]]
#    return "".join(a_list)
#
# def decrypt(a_string):
#    empty_string = ""
#    index1 = [-1, -1]
#    index2 = [-1, -1]
#    for i in range(0, len(a_string), 2):
#        for j in range(len(CIPHER)):
#            for k in range(len(CIPHER)):
#                if a_string[i] == CIPHER[j][k]:
#                    index1 = [j, k]
#                if a_string[i + 1] == CIPHER[j][k]:
#                    index2 = [j, k]
#        if (index1[0] == index2[0]):
#            index1[1] -= 1
#            index2[1] -= 1
#            if index1[1] == -1:
#                index1[1] = 4
#            if index2[1] == -1:
#                index2[1] = 4
#            empty_string += CIPHER[index1[0]][index1[1]]
#            empty_string += CIPHER[index2[0]][index2[1]]
#        # same column
#        elif (index1[1] == index2[1]):
#            index1[0] -= 1
#            index2[0] -= 1
#            if index1[0] == -1:
#                index1[0] = 4
#            if index2[0] == -1:
#                index2[0] = 4
#            empty_string += CIPHER[index1[0]][index1[1]]
#            empty_string += CIPHER[index2[0]][index2[1]]
#        else:
#            empty_string += CIPHER[index1[0]][index2[1]]
#            empty_string += CIPHER[index2[0]][index1[1]]
#    return empty_string
# # Below are some lines of code that will test your function.
# # You can change the value of the variable(s) to test your
# # function with different inputs.
# #
# # If your function works correctly, this will originally
#
# # print: QLGRQTVZIBTYQZ, then PSHELXOWORLDSX
#
# print(encrypt("PS. Hello, worlds"))
#
# print(decrypt("QLGRQTVZIBTYQZ"))

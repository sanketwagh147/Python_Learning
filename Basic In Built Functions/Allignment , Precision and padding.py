print("{2:!<20}|{3:!>20}|{1:20}|{0:20}".format("sanket", "wagh","sukanya", "patra"))
#{index_Location:any_char(< or ^ or >Total_characters)}

# Padding and precision in python
index = 0  # index is used to index item in format(0,1,2.n)
padding_character = "-"  # Any single character can be used as padding
alignment =">"  # # Alignment is < for left , ^ for center and > for right alignment
lengthOf_string = 10  # extend string to len 10 if not else do nothing
'{0:-^10}'.format("HELLO",padding_character,alignment,lengthOf_string)
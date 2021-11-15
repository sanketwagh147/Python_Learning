#The math we typically do is in base 10: adding 10 to one digit
#increments the next digit. Thus, the smallest (furthest right)
#number is the ones digit, the next smallest is the tens digit,
#the next smallest is the hundreds digit, etc. A 5 in the ones
#slot adds 5 to the total; a 5 in the tens slot adds 50 (5 * 10)
#to the total; a 5 in the hundreds slot adds 500 to the total
#(5 * 100), etc.
#
#Hexadecimal is a way of representing a different base, base 16.
#The digits 0 through 9 represent the normal numbers; A is 10,
#B is 11, C is 12, D is 13, E is 14, and F is 15. So, the
#hexadecimal number E is the standard number 14.
#
#Like base 10, hexadecimal has digit places: the ones digit, the
#16s digit, the 256s digit, and the 4096s digit. A 5 in the ones
#spot adds 5 to the total; in the 16s spot it adds 80 to the
#total (5 * 16), in the 256s spot it adds 1280 (5 * 256), and in
#the 4096s spot it adds 20480 (5 * 4096). In 4 digits, base 16
#can represent base 10 numbers up to 65,535 (16^4 - 1).
#
#Write a function called hex_to_decimal. hex_to_decimal will take
#one parameter, a string. You may assume the string will always
#have exactly 4 characters, and that all the characters will be
#a numeral from 0 to 9 or a capital letter from A to F. Return
#result of converting this hexadecimal number to a standard
#base-10 number.



#Add your code here!



#Below are some lines of code that will test your function.
#You can change the value of the variable(s) to test your
#function with different inputs.
#
#If your function works correctly, this will originally
#print: 43690, 65535, 4369, 4660, 17185, 0, 1885.
print(hex_to_decimal("AAAA"))
print(hex_to_decimal("FFFF"))
print(hex_to_decimal("1111"))
print(hex_to_decimal("1234"))
print(hex_to_decimal("4321"))
print(hex_to_decimal("0000"))
print(hex_to_decimal("075D"))



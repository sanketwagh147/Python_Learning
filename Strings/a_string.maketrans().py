

a_string = "ddddd   ooooo ggggg sssss"
# It converts into ordinal translation dictionary
translate_dict = str.maketrans("dog", "DOG")

# Usage

print(a_string.translate(translate_dict))
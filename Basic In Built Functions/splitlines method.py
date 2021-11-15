a_string = '''what the hell is goingh on \n am i going crazy \n or the world is crazy
really sad''' # line breaks which are implicitly mentioned also count to split
a_list = a_string.splitlines()
print(a_list)
# >>['what the hell is goingh on ', ' am i going crazy ', ' or the world is crazy', 'really sad']

# if the optional keyword parameter keepends=True the the \n is also included in the list
a_list2 = a_string.splitlines(keepends=True)
print(a_list2)
# >>['what the hell is goingh on \n', ' am i going crazy \n', ' or the world is crazy\n', 'really sad']

square = lambda a_int, b_int, c_int: a_int**a_int + b_int - c_int
y = square(2, 1, 2)
print(y)

# using lambda with map
a_list=[1,2,3,4,5]
a_list2=[1,2,3,4,5]
a_list3=[1,2,3,4,0]
new_list_2 = list(map(lambda x,y,z: x+y+z, a_list,a_list2, a_list3))

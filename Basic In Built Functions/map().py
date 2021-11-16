from icecream import ic

# making a list which passes each item on the list to a function and creates a new list.
a_list=[1,2,3,4,5]
a_list2=[1,2,3,4,5]
a_list3=[1,2,3,4,0]
def square(a_int):
    return a_int*a_int
new_list=list(map(square, a_list))
# print(new_list)
ic(new_list)
# using lambda with map
a_list=[1,2,3,4,5]
a_list2=[1,2,3,4,5]
a_list3=[1,2,3,4,5]
ic(a_list)
ic(a_list2)
ic(a_list3)
new_list_2 = list(map(lambda x,y,z: x+y+z, a_list,a_list2, a_list3))
ic(new_list_2)

square_list = list(map(lambda x: x * x, a_list))
ic(square_list)


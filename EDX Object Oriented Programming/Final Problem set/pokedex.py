class Pokemon:
    def __init__(self,Number,Name,Type1,Type2,HP,Attack,Defense,SpecialAtk,SpecialDef,Speed,Generation,Legendary,Mega):
        # self.l = str(Legendary).title
        # self.m = str(Mega).title
        self.Number = int(Number)
        self.Name = str(Name)
        self.Type1 = str(Type1)
        self.Type2 = str(Type2)
        self.HP = int(HP)
        self.Attack = int(Attack)
        self.Defense = int(Defense)
        self.SpecialAtk = int(SpecialAtk)
        self.SpecialDef = int(SpecialDef)
        self.Speed = int(Speed)
        self.Generation = int(Generation)
        self.Legendary = eval(Legendary)
        self.Mega = eval(Mega)
    def avg(self):
        return self.HP + self.Attack + self.Defense + self.SpecialAtk + self.SpecialDef + self.Speed/6
# new = Pokemon(1, "Bulbasaur", "Grass"," Poison",45,49,49,65,65,45,1,"FALSE".title(),"FALSE".title())
pokedex = open(r"C:\Users\Admin\PycharmProjects\Practice\Object Oriented Programming EDX\Final Problem set\samplePokemon.csv", "r")
data = pokedex.read().splitlines()[1:]
# print(data)
poke_list = []
for each in data:
    # print(each)
    data1 =[]
    data1 = each.split(",")
    poke_list.append(data1)
    # print(data1)
# print(poke_list)
pokemon_object_list = []
for i in range(0, len(poke_list)):
    # print(poke_list[i][1])
    # print(type(poke_list[i][1]))
    poke_list[i][1] = Pokemon(poke_list[i][0], poke_list[i][1], poke_list[i][2], poke_list[i][3], poke_list[i][4], poke_list[i][5],
                   poke_list[i][6], poke_list[i][7], poke_list[i][8], poke_list[i][9], poke_list[i][10], poke_list[i][11].title(), poke_list[i][12].title())
    # print(type(poke_list[i][1]))
    pokemon_object_list.append(poke_list[i][1])
# print(pokemon_object_list)
# How many Pokemon have only one type? In other words, for how many Pokemon is Type2 blank?
#count = 0
# for each in pokemon_object_list:
#
#     if each.Type2 == "":
#         count +=1
# print(count)

# What is the most common type? Include both Type1 and Type2 in your count.
# a_dict = {}
# for i in range(0, len(pokemon_object_list)):
#     if pokemon_object_list[i].Type1 not in a_dict.keys():
#         a_dict[pokemon_object_list[i].Type1] = 1
#     else:
#         a_dict[pokemon_object_list[i].Type1] += 1
# for i in range(0, len(pokemon_object_list)):
#     if pokemon_object_list[i].Type2 not in a_dict.keys():
#         if pokemon_object_list[i].Type2 !=" ":
#             a_dict[pokemon_object_list[i].Type2] = 1
#         else:
#             a_dict[pokemon_object_list[i].Type2] += 1
# #
# # print(a_dict)
# # print(max(a_dict.values()))
# # print(a_dict[max(a_dict, key=a_dict.get)])
# # print(max(a_dict, key=a_dict.get))
#
#
# Keymax = max(a_dict, key=a_dict.get)
# print(Keymax)

# What Pokemon has the highest HP statistic?
# hp_list =[[i.HP,i.Name,i.Legendary, i.Mega,i.Defense,i.Type1, i.Type2,i.Attack, i.SpecialAtk, i.SpecialDef,i.Speed] for i in pokemon_object_list]
# print(hp_list)
# Excluding Pokemon that are either Mega or Legendary, what Pokemon has the highest Defense statistic?
# non_megaNlegendary = []
# for i in range(0, len(hp_list)):
#     if hp_list[i][2] == False and hp_list[i][3] == False:
#         non_megaNlegendary.append(hp_list[i])
# # print(non_megaNlegendary)
# max_defense = max([(i[4],i[1]) for i in non_megaNlegendary])
# # print(max_defense)
#
# # Among Legendary Pokemon, what is the most common type? Include both Type1 and Type2 in your count.
# legendary_list = list(filter(lambda x: x[2] == True, hp_list))
#print(legendary_list)

# a_dict = {}
# for i in range(0, len(legendary_list)):
#     if legendary_list[i][5] not in a_dict.keys():
#         a_dict[legendary_list[i][5]] = 1
#     else:
#         a_dict[legendary_list[i][1]] += 1
# for i in range(0, len(legendary_list)):
#     if legendary_list[i][6] not in a_dict.keys():
#         if legendary_list[i][6] !=" ":
#             a_dict[legendary_list[i][6]] = 1
#         else:
#             a_dict[legendary_list[i][6]] += 1
# # print(a_dict)
# # print(max(a_dict.values()))
# # print(a_dict[max(a_dict, key=a_dict.get)])
# # print(max(a_dict, key=a_dict.get))
# Keymax = max(a_dict, key=a_dict.get)
# print(Keymax)

#In terms of the sum of all six stats (HP, Attack, Defense, Special Attack, Special Defense,
# and Speed), what is the weakest Legendary Pokemon? If there is a tie, list any of the tying Pokemon.
# for i in range(0, len(non_megaNlegendary)):
#     y = non_megaNlegendary[i][0]+non_megaNlegendary[i][4]+non_megaNlegendary[i][7]+non_megaNlegendary[i][8]+non_megaNlegendary[i][9]+non_megaNlegendary[i][10]
#     non_megaNlegendary[i].append(y)
# max1 = max([(i[-1],i[1]) for i in non_megaNlegendary])
# print(non_megaNlegendary)
# print(max1)

# hat type has the highest average Speed statistic? Include both Type1 and Type2 in your calculation.
# a_dict = {}
# for i in range(0, len(hp_list)):
#     if hp_list[i][5] not in a_dict.keys():
#         count = 1
#         a_dict[hp_list[i][5]] = [hp_list[i][10], count]
#     else:
#         count +=1
#         a_dict[hp_list[i][5]][0] += hp_list[i][10]
#         a_dict[hp_list[i][5]][1] += count
# for i in range(0, len(hp_list)):
#     if hp_list[i][6] not in a_dict.keys():
#         if hp_list[i][6] !=" ":
#             count = 1
#             a_dict[hp_list[i][6]] = [hp_list[i][10], count]
#         else:
#             a_dict[hp_list[i][6]][0] += hp_list[i][10]
#             a_dict[hp_list[i][6]][1] += 1
# # print(a_dict)
# # print(max(a_dict.values()))
# # print(a_dict[max(a_dict, key=a_dict.get)])
# # print(max(a_dict, key=a_dict.get))
# a_dict2 ={}
# for i in a_dict.keys():
#     avg = a_dict[i][0]/a_dict[i][1]
#     list3 = [avg, a_dict[i][0], a_dict[i][1]]
#     a_dict2[i] = list3
# print(a_dict2)
# Keymax = max(a_dict2, key=)
# print(Keymax)

# speed_list = [[i.Name, i.Type1, i.Type2,i.Speed] for i in pokemon_object_list]
# # print(speed_list)
# a_dict = {}
# for each in speed_list:
#     if each[1] not in a_dict.keys():
#         a_dict[each[1]] = [each[3],1 ]
#     else:
#         a_dict[each[1]][0] += each[3]
#         a_dict[each[1]][1] += 1
#     if each[2]
#         a_dict[each[2]] = [int(),int() ]
#
#         # print(each[1])
#         # print(each[2])
#         print(each[3])
#         a_dict[each[1]][0] += each[3]
#         a_dict[each[1]][1] += 1
#         a_dict[each[2]][0] += each[3]
#         a_dict[each[2]][1] += 1
#
# print(a_dict)
# Among all 7 Pokemon generations, which generation had the highest average sum of all six stats (HP, Attack, Defense, Special Attack, Special Defense, and Speed)?
# gen_list =[[i.Name,i.Generation,(i.HP+i.Defense+i.Attack+i.SpecialAtk+i.SpecialDef+i.Speed)/6] for i in pokemon_object_list]
# # print(gen_list)
# a_dict = {}
# for each in gen_list:
#     if each[1] not in a_dict.keys():
#         a_dict[each[1]] = []
#         a_dict[each[1]].append(each[2])
#         a_dict[each[1]].append(1)
#     else:
#         a_dict[each[1]][0] += each[2]
#         a_dict[each[1]][1] += 1
#
# print(a_dict)
# for each in a_dict.items():
#     avg = a_dict.values()
#     # print(avg)

mega_list =[[i.Number,i.Name,i.Mega,(i.HP+i.Defense+i.Attack+i.SpecialAtk+i.SpecialDef+i.Speed)/6] for i in pokemon_object_list]
# print(mega_list)
mega_filter = list(filter(lambda x: x[2] == True, mega_list))
# print(mega_filter)
mega_total = 0
for i in range(0, len(mega_filter)):
    mega_total += int(mega_filter[i][3])
mega_avg = mega_total/len(mega_filter)
# print(len(mega_filter))
# print(mega_avg)
mega_id_list = [i[0] for i in mega_filter]
# print(mega_id_list)
non_mega_count = 0
non_mega_avg = 0
for each in mega_list:
    # print(each[0],each[2])
    if each[0] in mega_id_list and each[2] == False:
        non_mega_avg += each[3]
        non_mega_count +=1
# print(non_mega_avg/non_mega_count)
# print(non_mega_avg/non_mega_count)
difference = mega_avg-(non_mega_avg/non_mega_count)
# print(difference)
d2 = mega_total - non_mega_avg
print(d2)

#ega_total = 0
# #or i in range(0, len(mega_filter)):
#     mega_total += int(mega_filter[i][3])
# mega_avg = mega_total/len(mega_filter)
# # print(len(mega_filter))
# # print(mega_avg)
# mega_id_list = [i[0] for i in mega_filter]
# # print(mega_id_list)
# non_mega_count = 0
# non_mega_avg = 0
# for each in mega_list:
#     # print(each[0],each[2])
#     if each[0] in mega_id_list and each[2] == False:
#         non_mega_avg += each[3]
#         non_mega_count +=1
# # print(non_mega_avg/non_mega_count)
# # print(non_mega_avg/non_mega_count)
# difference = mega_avg-(non_mega_avg/non_mega_count)
# # print(difference)
# d2 = mega_total - non_mega_avg
# print(d2)
# print(len(mega_list))

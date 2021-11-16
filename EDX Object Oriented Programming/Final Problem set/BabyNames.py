names_file = open('sample.csv', 'r')
data = names_file.read().split()

# To get length of data set
# print(len(data))

# How many total births are covered by the names in the database?
# print(data)
# data = names_file.read().split()
# data_list = []
# for each in data:
#     single_item = each.split(",")
#     data_list.append(single_item)
# # print(data_list)
# total_births = 0
# for each in data_list:
#     total_births += int(each[1])
# print(total_births)
#

# # What is the most common girl's name that begins with the letter Q?
# data_list = []
# a_dict = {}
# for each in data:
#     single_item = each.split(",")
#     data_list.append(single_item)
# # print(data_list)
# total_names = 0 # total names of boys starting with letter Z
# for i in range(0,len(data_list)):
#     # print("{} and {}".format(data_list[i][2], data_list[i][0][0]))
#     if data_list[i][2] == "Girl" and data_list[i][0][0] =="Q":
#
#         # print("{}".format(data_list[i][0]))
#         if data_list[i][0] not in a_dict.keys():
#             a_dict[data_list[i][0]] = 1
#         else:
#             a_dict[data_list[i][0]] += 1
# # print(a_dict)
# print(max(a_dict, key=a_dict.get))

#  How many total babies were given names that both start and end with vowels (A, E, I, O, or U)?
# data_list = []
# a_dict = {}
# vovel_list = ["A", "E", "I", "O", "U", "a", "e", "i", "o", "u"]
# total = 0 # counter for babies starting and ending with vowels.
# for each in data:
#     single_item = each.split(",")
#     data_list.append(single_item)
# # print(data_list)
# total_names = 0  # total names of boys starting with letter Z
# for i in range(0, len(data_list)):
#     # print("{} and {}, baby count:{}".format(data_list[i][0][0], data_list[i][0][-1], data_list[i][1]))
#     if data_list[i][0][0] in vovel_list and data_list[i][0][-1] in vovel_list:
#         # print(data_list[i][1])
#         total += int(data_list[i][1])
# print(total)

# What letter is the least common first letter of a baby's name (in terms of number of babies with names starting with that letter, not number of names)?
# data_list = []
# a_dict = {}
# for each in data:
#     single_item = each.split(",")
#     data_list.append(single_item)
# # print(data_list)
# total_names = 0  #
# for i in range(0, len(data_list)):
#     # print("{} , baby count:{}".format(data_list[i][0][0], data_list[i][0][-1], data_list[i][1]))
#     if data_list[i][0][0] not in a_dict.keys():
#         a_dict[data_list[i][0][0]] = int(data_list[i][1])
#     else:
#         a_dict[data_list[i][0][0]] += int(data_list[i][1])
# # print(a_dict)
# # print(min(a_dict, key=a_dict.get))

# How many babies were born with names starting with that least-common letter?
# data_list = []
# a_dict = {}
# for each in data:
#     single_item = each.split(",")
#     data_list.append(single_item)
# # print(data_list)
# total_names = 0  #
# for i in range(0, len(data_list)):
#     # print("{} , baby count:{}".format(data_list[i][0][0], data_list[i][0][-1], data_list[i][1]))
#     if data_list[i][0][0] not in a_dict.keys():
#         a_dict[data_list[i][0][0]] = int(data_list[i][1])
#     else:
#         a_dict[data_list[i][0][0]] += int(data_list[i][1])
# # print(a_dict)
# print(a_dict[min(a_dict, key=a_dict.get)])

# What letter is the most common first letter of a baby's name (in terms of number of babies with names starting with that letter, not number of names)?
# data_list = []
# a_dict = {}
# for each in data:
#     single_item = each.split(",")
#     data_list.append(single_item)
# # print(data_list)
# total_names = 0  #
# for i in range(0, len(data_list)):
#     # print("{} , baby count:{}".format(data_list[i][0][0], data_list[i][0][-1], data_list[i][1]))
#     if data_list[i][0][0] not in a_dict.keys():
#         a_dict[data_list[i][0][0]] = int(data_list[i][1])
#     else:
#         a_dict[data_list[i][0][0]] += int(data_list[i][1])
# # print(a_dict)
# print(max(a_dict, key=a_dict.get))

# How many babies were born with names starting with that most-common letter?
# data_list = []
# a_dict = {}
# for each in data:
#     single_item = each.split(",")
#     data_list.append(single_item)
# # print(data_list)
# total_names = 0  #
# for i in range(0, len(data_list)):
#     # print("{} , baby count:{}".format(data_list[i][0][0], data_list[i][0][-1], data_list[i][1]))
#     if data_list[i][0][0] not in a_dict.keys():
#         a_dict[data_list[i][0][0]] = int(data_list[i][1])
#     else:
#         a_dict[data_list[i][0][0]] += int(data_list[i][1])
# # print(a_dict)
# print(a_dict[max(a_dict, key=a_dict.get)])

# By default, the Social Security Administration's data separates out names by gender. For example,
# Jamie is listed separately for girls and for boys. If you were to remove this separation,
# what would be the most common name in the 2010s regardless of gender?
# data_list = []
# a_dict = {}
# for each in data:
#     single_item = each.split(",")
#     data_list.append(single_item)
# # print(data_list)
# total_names = 0 # total names of boys starting with letter Z
# for i in range(0,len(data_list)):
#     # print("{} and {}".format(data_list[i][2], data_list[i][0][0]))
#     if data_list[i][0] not in a_dict.keys():
#         a_dict[data_list[i][0]] = int(data_list[i][1])
#     else:
#         a_dict[data_list[i][0]] += int(data_list[i][1])
# print(max(a_dict, key=a_dict.get))

# How many people would have that name?
# data_list = []
# a_dict = {}
# for each in data:
#     single_item = each.split(",")
#     data_list.append(single_item)
# # print(data_list)
# total_names = 0 # total names of boys starting with letter Z
# for i in range(0,len(data_list)):
#     # print("{} and {}".format(data_list[i][2], data_list[i][0][0]))
#     if data_list[i][0] not in a_dict.keys():
#         a_dict[data_list[i][0]] = int(data_list[i][1])
#     else:
#         a_dict[data_list[i][0]] += int(data_list[i][1])
# print(a_dict[max(a_dict, key=a_dict.get)])

# What name that is used for both genders has the smallest difference in which gender holds the name most frequently?
# In case of a tie, enter any one of the correct answers.
data_list = []
a_dict = {}
for each in data:
    single_item = each.split(",")
    data_list.append(single_item)
# print(data_list)
total_names = 0 # total names of boys starting with letter Z
for i in range(0,len(data_list)):
    # print("{} and {}".format(data_list[i][2], data_list[i][0][0]))
    if data_list[i][0] not in a_dict.keys():
        a_dict[data_list[i][0]] = [0, 0]
        #print(data_list[i][0])
        if data_list[i][2] == "Boy":
            a_dict[data_list[i][0]][0] = int(data_list[i][1])
        else:
            a_dict[data_list[i][0]][1] = int(data_list[i][1])
    else:
        if data_list[i][2] == "Boy":
            a_dict[data_list[i][0]][0] += int(data_list[i][1])
        else:
            a_dict[data_list[i][0]][1] += int(data_list[i][1])
# print(a_dict)
list2 =[]
for each in a_dict.keys():

    if a_dict[each][0] >0 and a_dict[each][1]>0:
        list1 = []
        difference = abs(a_dict[each][0] - a_dict[each][1])
        # print("test")
        list1 = [each, difference]
        list2.append(list1)

# print(min(list2)
print(min(list2, key=lambda x: x[1]))
# list3 = [['Isabella', 42511], ['Sophia', 42213], ['Jacob', 42115], ['Emma', 35903], ['Ethan', 34483], ['Mason', 34032], ['William', 34081], ['Olivia', 34085], ['Jayden', 31445], ['Michael', 33769], ['Noah', 32943], ['Alexander', 32216], ['Daniel', 30854], ['Aiden', 30670], ['Ava', 30731], ['Anthony', 29565], ['Joshua', 28920], ['Emily', 28368], ['Matthew', 28061], ['Elijah', 27557], ['Abigail', 27327], ['Andrew', 27309], ['David', 27184], ['Christopher', 27060], ['James', 26872], ['Logan', 25745], ['Joseph', 26510], ['Madison', 25349], ['Benjamin', 25266], ['Gabriel', 24865], ['Liam', 24219], ['Jackson', 23996], ['Ryan', 22396], ['Samuel', 23064], ['John', 22404], ['Christian', 20956], ['Jonathan', 21199], ['Lucas', 20647], ['Caleb', 20308], ['Dylan', 19087], ['Elizabeth', 20154], ['Landon', 20082], ['Addison', 19165], ['Tyler', 18793], ['Gavin', 18533], ['Evan', 18093], ['Nicholas', 18098], ['Brayden', 17957], ['Isaiah', 16895], ['Carter', 16330], ['Owen', 16419], ['Brandon', 16243], ['Angel', 13184], ['Jordan', 12863], ['Jeremiah', 15175], ['Julian', 15026], ['Aaron', 14938], ['Alexis', 11608], ['Adrian', 14349], ['Cameron', 13160], ['Hunter', 14225], ['Jose', 14388], ['Avery', 10496], ['Austin', 13673], ['Eli', 13609], ['Brooklyn', 13049], ['Chase', 12413], ['Levi', 12466], ['Aubrey', 12201], ['Zoe', 12448], ['Nevaeh', 12380], ['Ashley', 11597], ['Ayden', 10898], ['Taylor', 9196], ['Dominic', 10638], ['Riley', 3474], ['Josiah', 10355], ['Cooper', 10187], ['Blake', 9695], ['Brody', 10038], ['Carson', 9619], ['Parker', 8449], ['Peyton', 4694], ['Tristan', 9350], ['Bentley', 8780], ['Hayden', 5149], ['Jaxon', 8483], ['Alex', 8089], ['Jaden', 7661], ['Sydney', 8124], ['Aidan', 7872], ['Nolan', 7786], ['Morgan', 6734], ['Mackenzie', 7570], ['Bryson', 7254], ['Trinity', 7199], ['Harper', 6522], ['Grayson', 7008], ['Micah', 6651], ['Andrea', 7015], ['Kayden', 5818], ['Bailey', 6500], ['Kaden', 6770], ['Bryce', 6604], ['Kyle', 6703], ['Genesis', 6639], ['Ashton', 6321], ['Giovanni', 6698], ['Payton', 5109], ['Ryder', 6458], ['Easton', 6375], ['Caden', 6341], ['Jace', 6296], ['Hudson', 6142], ['Brady', 6191], ['Asher', 6146], ['Jesse', 6008], ['Preston', 6053], ['Kennedy', 5764], ['London', 5055], ['Rylee', 5211], ['Gabrielle', 5697], ['Jonah', 5550], ['Jordyn', 4665], ['Jade', 5246], ['Devin', 4948], ['Cayden', 4881], ['Reagan', 4628], ['Kendall', 4089], ['Wesley', 4814], ['Rylan', 4051], ['Braxton', 4716], ['Jude', 4591], ['Kaiden', 4549], ['Reese', 3634], ['Cody', 4534], ['Camden', 4246], ['Kylee', 4415], ['Sawyer', 3646], ['Mckenzie', 4291], ['Maddox', 4183], ['Jaiden', 3556], ['Tanner', 4131], ['Bradley', 4102], ['Lincoln', 3973], ['Skylar', 2891], ['Jaylen', 3000], ['Kai', 2937], ['Shane', 3431], ['Eden', 2953], ['Ryleigh', 3270], ['Israel', 3140], ['Hadley', 3100], ['Ezra', 2985], ['Greyson', 3105], ['Shelby', 3030], ['Spencer', 2958], ['Griffin', 3050], ['Corbin', 3029], ['Chance', 2976], ['Kinley', 2943], ['Zion', 2082], ['Quinn', 607], ['Charlie', 1414], ['Jameson', 2786], ['Ariel', 2086], ['Aria', 2825], ['Shawn', 2826], ['Leslie', 2740], ['Delaney', 2776], ['Keegan', 2521], ['Erin', 2671], ['Teagan', 2125], ['Andy', 2705], ['Bennett', 2562], ['Jayce', 2582], ['Kyler', 2489], ['Drew', 2300], ['Kelsey', 2560], ['Luca', 2481], ['Londyn', 2543], ['Amir', 2559], ['Presley', 2323], ['Marley', 2165], ['Kameron', 2332], ['Skyler', 1242], ['Cadence', 2342], ['Cheyenne', 2486], ['Caiden', 2453], ['Kaydence', 2397], ['Brennan', 2277], ['Jasper', 2377], ['Cassidy', 2295], ['Paxton', 2271], ['Aden', 2315], ['Elliot', 1843], ['Lane', 2199], ['Judah', 2246], ['Reid', 2214], ['Camryn', 1727], ['Colby', 2092], ['Dakota', 53], ['Emery', 1554], ['Dawson', 2119], ['Finn', 2139], ['Anderson', 2066], ['Emerson', 785], ['Cruz', 2030], ['Elliott', 1677], ['Kamryn', 1586], ['Amari', 820], ['Corey', 1976], ['Kelly', 1783], ['Rowan', 838], ['Heaven', 1933], ['Dallas', 1495], ['Dillon', 1878], ['Carmen', 1844], ['Paris', 1754], ['Rylie', 1774], ['Tatum', 1270], ['Guadalupe', 1646], ['Devon', 1646], ['Braylen', 1714], ['Sasha', 1733], ['Jett', 1760], ['Nehemiah', 1725], ['Beckett', 1732], ['Tristen', 1648], ['Lyric', 1260], ['Kellen', 1663], ['Imani', 1596], ['Finley', 732], ['Courtney', 1391], ['Ali', 875], ['Kellan', 1572], ['Jaelyn', 1476], ['Beau', 1561], ['Journey', 1473], ['Keaton', 1497], ['Baylee', 1547], ['Jaime', 1400], ['Brooks', 1527], ['Kaylin', 1520], ['Karson', 1428], ['Reed', 1499], ['Jamie', 934], ['Landyn', 1416], ['Phoenix', 611], ['Brylee', 1405], ['Tate', 1376], ['Harley', 627], ['Jalen', 1361], ['Braelyn', 1204], ['August', 1122], ['Jamari', 1270], ['Casey', 394], ['Kadence', 1207], ['Karter', 1140], ['Brantley', 1237], ['Sage', 758], ['Davis', 1245], ['Kassidy', 1238], ['River', 720], ['Reece', 821], ['Bristol', 1195], ['Brett', 1200], ['Skye', 1093], ['Charlee', 1186], ['Joy', 1169], ['Kobe', 1169], ['Porter', 1151], ['Kenley', 1107], ['Mckinley', 1029], ['Miracle', 1134], ['Amare', 1087], ['Jaycee', 1065], ['Alijah', 1075], ['Chandler', 876], ['Noel', 806], ['Orion', 1099], ['Jaylynn', 1072], ['Dana', 1036], ['Ryland', 1053], ['Barrett', 1030], ['Adriel', 1043], ['Sam', 1062], ['Justice', 1], ['Rhys', 1006], ['Kamden', 1000], ['Aspen', 933], ['Armani', 337], ['Amani', 821], ['Jamison', 937], ['Kieran', 920], ['Ari', 751], ['Remington', 772], ['Dorian', 951], ['Leighton', 562], ['Terry', 954], ['Tori', 944], ['Brodie', 926], ['Raven', 893], ['Haven', 654], ['Jaydon', 913], ['Nico', 868], ['Shiloh', 615], ['Kasen', 902], ['Gianni', 758], ['Keagan', 773], ['Kristian', 819], ['Boston', 845], ['Milan', 613], ['Kamari', 441], ['Quincy', 652], ['Kourtney', 851], ['Uriah', 836], ['Asa', 807], ['Madden', 763], ['Briley', 720], ['Jaylin', 218], ['Sullivan', 794], ['Raiden', 823], ['Sidney', 357], ['Layne', 663], ['Taryn', 805], ['Lawson', 799], ['Dayton', 786], ['Jessie', 84], ['Diamond', 757], ['Harlow', 780], ['Blaine', 784], ['Joey', 614], ['Shannon', 609], ['Cory', 760], ['Bently', 759], ['Charley', 605], ['Royce', 731], ['Jordynn', 727], ['Callen', 726], ['Kody', 721], ['Layton', 671], ['Rene', 702], ['Jadyn', 345], ['Karsyn', 587], ['Messiah', 634], ['Francis', 641], ['Sincere', 587], ['Kaya', 693], ['Omari', 704], ['Tristin', 659], ['Channing', 368], ['Aydan', 664], ['Memphis', 581], ['Semaj', 514], ['Jensen', 634], ['Rory', 183], ['Aydin', 687], ['Kylan', 634], ['Darian', 647], ['Lee', 652], ['Aidyn', 598], ['Makai', 655], ['Jorden', 581], ['Elisha', 398], ['Aryan', 613], ['Jasiah', 598], ['Ronnie', 614], ['Regan', 550], ['Kolby', 596], ['Soren', 628], ['Arya', 462], ['Camren', 616], ['Kaylen', 551], ['Toby', 535], ['Kendal', 472], ['Lamar', 575], ['Campbell', 299], ['Jaidyn', 152], ['Ryann', 598], ['Kaeden', 604], ['Rayne', 535], ['Ellis', 291], ['Kayson', 588], ['Tegan', 393], ['Luka', 578], ['Kasey', 293], ['Bentlee', 446], ['Adrien', 575], ['Sterling', 487], ['Rayan', 521], ['Bryn', 563], ['Mina', 557], ['Akira', 522], ['Killian', 554], ['Averi', 558], ['Jaeden', 517], ['Van', 545], ['Jaylyn', 439], ['Saige', 524], ['Zuri', 532], ['Kymani', 404], ['Kensley', 529], ['Stacy', 500], ['Bo', 511], ['Caydence', 511], ['Sloan', 394], ['Brogan', 492], ['Payten', 445], ['Damaris', 497], ['Lennon', 329], ['Dominique', 22], ['Frankie', 270], ['Landry', 95], ['Mayson', 425], ['Nova', 430], ['Sky', 332], ['Ashtyn', 355], ['Blakely', 453], ['Hayes', 469], ['Azariah', 255], ['Justus', 448], ['Devyn', 101], ['Alden', 451], ['Deven', 463], ['Blair', 341], ['Crosby', 441], ['Jean', 353], ['Emory', 121], ['Lennox', 411], ['Remy', 172], ['Noor', 405], ['Raylan', 417], ['Winter', 431], ['Noa', 309], ['Kori', 408], ['Rowen', 322], ['Devan', 375], ['Sonny', 403], ['Joelle', 411], ['Zaire', 361], ['Unique', 411], ['Camdyn', 121], ['Vaughn', 414], ['Kaidence', 397], ['Ellison', 369], ['Promise', 405], ['Trystan', 383], ['Legend', 400], ['Rylen', 352], ['Harlee', 399], ['Jaydin', 295], ['Gracyn', 395], ['Blaise', 393], ['Remi', 289], ['Carsen', 347], ['Haiden', 222], ['Nixon', 383], ['Damari', 350], ['Berkley', 342], ['Jordin', 197], ['Miller', 331], ['Jaydan', 322], ['Kingsley', 319], ['Marin', 363], ['Yael', 175], ['Fallon', 338], ['Jalynn', 361], ['Brecken', 331], ['Kadyn', 243], ['Wren', 327], ['Graysen', 341], ['Dani', 331], ['Emani', 350], ['Callan', 322], ['Eliot', 333], ['Kamren', 340], ['Destin', 349], ['Braylin', 184], ['Daylen', 337], ['Shea', 99], ['Dillan', 325], ['Arden', 242], ['Stevie', 305], ['Arian', 310], ['Jordon', 336], ['Mika', 300], ['Sunny', 236], ['Jailyn', 286], ['Langston', 293], ['Maison', 304], ['Karsen', 227], ['Adison', 309], ['Justine', 317], ['Briar', 172], ['Colbie', 303], ['Braedyn', 305], ['Lucca', 264], ['Jaedyn', 37], ['Kooper', 300], ['Scout', 220], ['Kacey', 275], ['Oakley', 53], ['Elia', 298], ['Stacey', 276], ['Carsyn', 101], ['Kamdyn', 101], ['Dion', 290], ['Zyaire', 253], ['Brandy', 277], ['Taylin', 247], ['Corbyn', 281], ['Canaan', 292], ['Jael', 55], ['Harlan', 284], ['Kyree', 239], ['Ryley', 45], ['Austyn', 18], ['Kyrie', 149], ['Sammy', 283], ['Zyon', 247], ['Korbyn', 255], ['Rilee', 268], ['Jai', 239], ['Reilly', 26], ['Baylor', 217], ['Chevy', 229], ['Robin', 94], ['Kylen', 254], ['Santana', 171], ['Austen', 242], ['Kaidyn', 99], ['Ayan', 240], ['Joan', 168], ['Collins', 174], ['Flynn', 260], ['Royal', 237], ['Avi', 215], ['Sandy', 259], ['Ely', 246], ['Darby', 202], ['Tayler', 213], ['Mikah', 166], ['Darcy', 257], ['Keller', 255], ['Andi', 216], ['Kalani', 137], ['Jaylan', 217], ['Sami', 240], ['Alexi', 193], ['Leyton', 235], ['Halo', 241], ['Perry', 203], ['Tristyn', 80], ['Haidyn', 211], ['Holland', 213], ['Aven', 13], ['Denver', 165], ['Ivory', 207], ['Nikita', 77], ['Brighton', 119], ['Shayne', 137], ['Britton', 97], ['Ever', 57], ['Dior', 174], ['Jalyn', 133], ['Elan', 201], ['Sutton', 119], ['Henley', 156], ['Denis', 210], ['Kaysen', 195], ['Keelan', 207], ['Johnnie', 190], ['Jackie', 80], ['Brook', 198], ['Zakaria', 153], ['Rhyan', 122], ['Ira', 153], ['Monroe', 155], ['Greysen', 204], ['Rosario', 193], ['Tracy', 85], ['Grey', 174], ['Kalen', 185], ['Teegan', 32], ['Emmerson', 198], ['Lyndon', 201], ['Myka', 187], ['Iman', 191], ['Marion', 14], ['Chayse', 142], ['Demari', 193], ['Zephaniah', 182], ['Loren', 71], ['Rylin', 95], ['Adler', 189], ['Laken', 78], ['Lynn', 168], ['Taytum', 154], ['Brentley', 190], ['Finnley', 67], ['Rian', 48], ['Jakai', 185], ['Khamari', 144], ['Chayce', 177], ['Syncere', 150], ['Rio', 96], ['Kaylan', 169], ['Rain', 145], ['Shay', 64], ['Dereon', 110], ['Amarie', 145], ['Carrington', 156], ['Murphy', 149], ['Payson', 93], ['Braxtyn', 171], ['Kaedyn', 110], ['Kiran', 121], ['Raleigh', 35], ['Rhylee', 178], ['Amauri', 139], ['Ramsey', 100], ['Raine', 167], ['Sailor', 173], ['Shia', 80], ['Gray', 148], ['Micaiah', 93], ['Harlem', 133], ['Kimani', 107], ['Hollis', 80], ['Aries', 90], ['Justyce', 133], ['Zia', 158], ['Cameryn', 101], ['Hartley', 153], ['Kaydin', 126], ['Masyn', 133], ['Honor', 93], ['Izel', 142], ['Makiah', 154], ['Azriel', 112], ['Sol', 83], ['Caelan', 138], ['Aarya', 139], ['Dyllan', 111], ['Karol', 110], ['Montana', 118], ['Palmer', 100], ['Nikola', 150], ['Quinlan', 101], ['Divine', 90], ['Afton', 137], ['Jayme', 107], ['Emry', 93], ['Daylin', 28], ['Kylar', 98], ['Shae', 123], ['Jessi', 129], ['Irie', 140], ['Yarel', 132], ['Zyion', 125], ['Berkeley', 132], ['Kendell', 73], ['Marlo', 78], ['Unknown', 33], ['Lux', 119], ['Tai', 122], ['Laine', 86], ['Rilyn', 134], ['Kodi', 69], ['Adair', 112], ['Jaydyn', 65], ['Kemari', 108], ['Nour', 114], ['Kameryn', 38], ['Charly', 73], ['Lyrik', 51], ['Reign', 78], ['Ocean', 50], ['Daelyn', 72], ['Marlowe', 113], ['Anay', 112], ['Jody', 86], ['Jules', 35], ['Tamar', 107], ['Isa', 28], ['Marlin', 89], ['Gracen', 33], ['Dakotah', 59], ['Conley', 111], ['Seven', 74], ['Adley', 112], ['Dream', 119], ['Samari', 90], ['Zyair', 115], ['Braylynn', 117], ['Montgomery', 115], ['Mckay', 114], ['Gentry', 21], ['Mykah', 36], ['Camari', 55], ['Taylen', 15], ['Wylie', 106], ['Khai', 105], ['Kaelin', 108], ['Krishna', 80], ['Reegan', 104], ['Kiernan', 98], ['Kylin', 0], ['Jaziah', 17], ['Dakoda', 75], ['Osiris', 92], ['Paiton', 107], ['Tylee', 103], ['Cadyn', 95], ['Shalom', 55], ['Tenzin', 29], ['Damani', 71], ['Brailyn', 83], ['Jariah', 99], ['Salem', 6], ['Arie', 61], ['Armoni', 44], ['Raylen', 66], ['Bryar', 86], ['Denim', 79], ['Khamani', 65], ['Lian', 69], ['Zyan', 92], ['Yuri', 17], ['Ezrah', 92], ['Jaidan', 95], ['Kerry', 60], ['Legacy', 68], ['Haydn', 96], ['Linden', 13], ['Indigo', 85], ['Jovi', 90], ['Keelyn', 91], ['Kelby', 55], ['Kolbie', 93], ['Zamari', 74], ['Macyn', 97], ['Ashten', 91], ['Jessiah', 92], ['Krystian', 92], ['Keilyn', 84], ['Amaree', 47], ['Gracin', 92], ['Jeriah', 90], ['Sora', 94], ['Kamil', 82], ['Rhiley', 75], ['Rowyn', 76], ['Jessy', 45], ['Kasyn', 87], ['Ami', 79], ['Lake', 87], ['Tru', 4], ['Onyx', 76], ['Caidyn', 56], ['Dempsey', 80], ['Oaklee', 80], ['Raylin', 69], ['Aly', 80], ['Amor', 82], ['Eliyah', 52], ['Aris', 43], ['Michal', 32], ['Ahmari', 66], ['Auden', 58], ['Issa', 73], ['Payden', 16], ['Tommie', 84], ['Ziyon', 83], ['Larkin', 56], ['Ashtin', 83], ['Cedar', 49], ['Rivers', 46], ['Imari', 38], ['Jacy', 81], ['Kamani', 43], ['Storm', 39], ['Greer', 72], ['Taegan', 52], ['Kris', 73], ['Lael', 67], ['Teagen', 12], ['Jadin', 71], ['Shayden', 69], ['Kirby', 52], ['Laiken', 59], ['Arin', 39], ['Prestyn', 75], ['Emari', 8], ['Ren', 67], ['Dailyn', 60], ['Lexington', 49], ['Charleston', 59], ['Shaya', 53], ['Evyn', 39], ['Elie', 57], ['Eastyn', 33], ['Ollie', 39], ['Dusty', 66], ['Halen', 34], ['Jaxyn', 61], ['Arley', 44], ['Brantlee', 66], ['Taylan', 53], ['Kobi', 50], ['Quin', 45], ['Talyn', 16], ['Aryn', 65], ['Breckyn', 65], ['Kelley', 51], ['Jacky', 59], ['Kalin', 33], ['Ryen', 14], ['Michel', 40], ['Ridley', 45], ['Shai', 30], ['Indiana', 29], ['Keylin', 60], ['Jaelin', 25], ['Dasani', 60], ['Denali', 54], ['Londen', 53], ['Eliah', 44], ['Mylan', 41], ['Surya', 59], ['Amore', 61], ['Crimson', 53], ['Bralyn', 44], ['Kamrin', 58], ['Lakota', 9], ['Jireh', 11], ['Khari', 45], ['Mycah', 29], ['Wynn', 33], ['Lakin', 50], ['Adel', 54], ['Callahan', 47], ['Dru', 37], ['Azari', 55], ['Kaelan', 54], ['Christen', 23], ['Schuyler', 40], ['Torrance', 45], ['Marlow', 31], ['Braylyn', 3], ['Cai', 43], ['Kamauri', 28], ['Loghan', 25], ['Naveen', 42], ['Tory', 16], ['Embry', 8], ['Merritt', 7], ['Alix', 45], ['An', 36], ['Dylann', 32], ['Shilo', 42], ['Koi', 40], ['Armonie', 49], ['Caylen', 46], ['Atley', 17], ['Bowie', 47], ['Tennyson', 40], ['Rhylan', 25], ['Wisdom', 7], ['Blayke', 1], ['Maysen', 3], ['Amarii', 27], ['Deniz', 42], ['Daryn', 32], ['Sammie', 7], ['True', 0], ['Jourdan', 38], ['Amen', 30], ['Arlen', 35], ['Aziah', 14], ['Graycen', 21], ['Kemani', 25], ['Carlin', 13], ['Elon', 35], ['Jae', 27], ['Micha', 37], ['Kailan', 34], ['Quincey', 25], ['Teigan', 0], ['Gabriele', 19], ['Riyan', 14], ['Carlisle', 33], ['Jalin', 36], ['Christin', 31], ['Jalani', 27], ['Kodie', 34], ['Lynden', 5], ['Neko', 33], ['Samar', 15], ['Bostyn', 29], ['Codi', 31], ['Jasiyah', 16], ['Nicola', 13], ['Damoni', 26], ['Skylor', 37], ['Valentine', 16], ['Kobie', 32], ['Aaryn', 24], ['Ashby', 21], ['Haydin', 22], ['Justis', 35], ['Kaylor', 22], ['Keelin', 31], ['Seneca', 18], ['Britain', 14], ['Pacey', 33], ['Truth', 19], ['Kailen', 4], ['Zaylin', 11], ['Adi', 16], ['Cortney', 17], ['Haedyn', 22], ['Jaydee', 29], ['Tracey', 26], ['Desi', 19], ['Hadyn', 11], ['Pheonix', 23], ['Carey', 30], ['Morgen', 26], ['Nana', 16], ['Merlin', 27], ['Timber', 14], ['Yuki', 27], ['Ziah', 24], ['Khali', 9], ['Eh', 18], ['Ellington', 15], ['Majesty', 18], ['Praise', 25], ['Shamari', 14], ['Kenyatta', 24], ['Tylar', 2], ['Akari', 21], ['Phoenyx', 23], ['Roni', 16], ['Tamari', 25], ['Zakariah', 23], ['Kimari', 8], ['Nazareth', 1], ['Amarri', 22], ['Mica', 1], ['Devine', 18], ['Kendel', 15], ['Wrigley', 21], ['Avry', 2], ['Clarke', 4], ['Lior', 21], ['Trinidad', 13], ['Cypress', 5], ['Gabriell', 4], ['Jamey', 3], ['Rayn', 17], ['Cashmere', 15], ['Freedom', 20], ['Hudsyn', 12], ['Hanley', 6], ['Nyjah', 12], ['Dannie', 11], ['Haydyn', 8], ['Braelin', 16], ['Ekam', 4], ['Jazz', 15], ['Lou', 16], ['Abriel', 5], ['Codie', 17], ['Paxtyn', 4], ['Kamori', 16], ['Toryn', 11], ['Ayomide', 11], ['Adama', 13], ['Kemoni', 10], ['Avyn', 11], ['Gurnoor', 3], ['Kaydyn', 6], ['Arlin', 5], ['Zacari', 12], ['Abrar', 4], ['Baylin', 6], ['Domonique', 6], ['Jaylenn', 12], ['Child', 7], ['Ryver', 8], ['Atlee', 1], ['Sacha', 10], ['Rei', 6], ['Taygen', 3], ['Amel', 8], ['Indy', 6], ['Kamoni', 5], ['Skylan', 8], ['Mackinley', 1], ['Keylen', 0], ['Dawsyn', 2], ['Jaye', 7], ['Baby', 6], ['Tatem', 0], ['Coley', 3], ['Kelyn', 6], ['Rogue', 2], ['Daylyn', 3], ['Averey', 5], ['Caelin', 4], ['Kimoni', 3], ['Callaway', 3], ['Kamarii', 3]]


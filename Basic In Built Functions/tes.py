def reader(a_file):
    file = open(a_file, "r")
    listy = file.readlines()
    file.close()         # Always close if not using with
    # print(listy)
    # print(type(listy))
    return_list = []
    for lines in listy:
        # print(lines)
        a_list = list(lines.split())
        # print(a_list)
        short_list = []
        
        for each in range(0, len(a_list)):
            # print(a_list[each])
            if a_list[each].isdigit() :
                each_int = int(a_list[each])
                # print(each_int)
                short_list.append(each_int)
            elif "." in a_list[each]:
                each_float = float(a_list[each])
                short_list.append(each_float)
            else:
                short_list.append(a_list[each])
            tuply = tuple(short_list)
        # print(tuply)
        return_list.append(tuply)   # Need to append tuple to results list
        
    print(return_list)

    return return_list              # Return the resulting list

reader(r'/practice code/Edx Coding Problems/Data Structures/sample.cs1301')

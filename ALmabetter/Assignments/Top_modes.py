def top_modes(a_list):
    import numpy as np
    unique, index, counts = np.unique(a_list, return_counts=True, return_index= True)
    # print(unique, "unique")
    # print(counts, "counts")
    # print(index, "index")
    c = a_list.count(a_list[1])
    # print(c)
    r = [ unique[i] for i in range(len(unique)) if counts[i] == max(counts) ]
    # print(r)
    for i in r:
        print("MOde are:", i)
    
    
a_list = [1,1,2,2,3,4,4]

top_modes(a_list)
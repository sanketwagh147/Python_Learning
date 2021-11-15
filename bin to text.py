with open(r"C:\Users\Admin\Desktop\Ka_KASPR_SPECTRA_20150728-204847.zpf", mode='rb') as file: # b is important -> binary
    fileContent = file.read()
    listy = fileContent.split()
    print(listy)



M =[[55,2,3,4],
    [1,55,3,4],
    [1,2,55,4],
    [1,2,55,44]]

x = [J for i in M for J in i]
print(x)

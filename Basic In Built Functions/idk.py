gradebook =[{"name": "David", "test1": 1, "test2": 5, "exam": 7},{"name": "David1", "test1": 123, "test2": 132, "test3": 311},{"name": "David2", "test1": 11, "test2": 11, "test3": 111}]
gradebook[0]["exam"] = 100
print(gradebook)
new_gradebook = {}
new_gradebook[gradebook[0]["name"]] = gradebook[0]
print(new_gradebook)

foo = ["sanket", "great", ["programmer"], "the", "foo", "bar"]
from icecream import ic

slice_foo = foo[1:3]

# foo[1] = "not great"
# foo[2] = foo[2].append("append")
foo[2].append("append")
# print(id(slice_foo[1]))
# print(id(foo[2]))
# print(foo)
# print(slice_foo)


for each in foo:
    # print(id(each))
    for item in slice_foo:
        if id(each) == id(item):
            # print(each, item, "has same id", id(each))
            pass
        else:
            # print("no match")
            ...

        # print(id(each))

# print([0, 1] + [8, 0])
# print([0, 1].append([8, 0]))
# print([0,1].extend([8,0])

#
temp = [1, 2]
temp_mul = temp * 8
# print(temp)

# what if we modify temp
temp = [1, 3]

# print(temp_mul)
# print(temp)


# extend copies reference
foo = [
    1,
    2,
    3,
]
bar = [4, 5, 6]

foo_id = [id(i) for i in foo]
bar_id = [id(i) for i in bar]
ic(bar_id, "bar id")
ic([(i, j) for i, j in zip(foo, foo_id)])
foo.extend(bar)
# foo_id.extend()
foo_id = [id(i) for i in foo]

ic([(i, j) for i, j in zip(foo, foo_id)])

# reference is copied

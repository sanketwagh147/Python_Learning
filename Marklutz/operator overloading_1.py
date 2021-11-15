class test():
    data = "spam"
    def __init__(self,value):
        self.value = value
        # self.li = [li]
    def __add__(self, other):
        return test(self.value + other)
    def __mul(self, other):
        return self.value * other.value
    def __getitem__(self, item):
        return self.data[item]
    # def __setitem__(self,index,value):
    #     self.data[index] = value
x = test(2)
x.k = "hkk"
x[1]

for item in x:
    print(item)

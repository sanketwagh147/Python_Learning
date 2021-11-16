import pandas as pd

data = [
            ['tom', 10, -100,1],
            ['nick', 15, 150,1],
            ['juli', 14, 140,1],
            ['tom', 19, 190,1],
            ['nick', 17, 170,1],
            ['juli', 11, 110,11]
        ]

df = pd.DataFrame(data, columns = ['Name', 'Age','AgeMultiplied','Random'])

print(df.corr())
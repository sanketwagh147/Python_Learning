import pandas as pd
li = [1,2,3]
li = pd.Series(li)
li.to_frame()
print("type", type)
print("li", li)
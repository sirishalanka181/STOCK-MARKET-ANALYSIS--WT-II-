import pandas as pd
df=pd.read_csv("nifty.csv")
data=df['Close'].loc[:]
data=list(data)
print(data)

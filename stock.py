import numpy as np
import pandas as pd
import quandl
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression
df = pd.read_csv('FB.csv')
print(df.head())

dates=[]
prices=[]
df['Date'] = pd.to_datetime(df['Date'])
df_date=df.loc[:,'Date']
df_close=df.loc[:,'Close']

for date in df_date:
    dates.append(date.toordinal())
for close_price in df_close:
    prices.append(close_price)

print(dates)
print(prices)

dates=np.array(dates)
dates=dates.reshape(-1,1)
dates_test=[]
for i in range(730):
    dates_test.append(dates[-1]+i)
print(dates_test)

svr_lin=SVR(kernel='rbf',degree=10,C=1e3)
svr_lin.fit(dates,prices)
plt.scatter(dates,prices,color="black",label="Data")
plt.scatter(dates_test,svr_lin.predict(dates_test),color="red",label="SVR")
plt.xlabel="Date"
plt.ylabel="Price"
plt.legend()
plt.show()

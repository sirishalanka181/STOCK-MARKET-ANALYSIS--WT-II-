import csv 
import pandas as pd 
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, jsonify
import numpy as np
import datetime
import matplotlib.pyplot as plt
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split 


app=Flask(__name__)
def get_usd():
     names=[]
     prices=[]
     changes=[]
     percentChanges=[]
     CryptoCurrenciesUrl = "https://in.finance.yahoo.com/currencies"
     r= requests.get(CryptoCurrenciesUrl)
     data=r.text
     soup=BeautifulSoup(data,features="html.parser")
     
     for listing in soup.find_all('tr', attrs={'data-reactid':40}):
          for name in listing.find_all('td', attrs={'data-reactid':40+3}):
               names.append(name.text)
          for price in listing.find_all('td', attrs={'data-reactid':40+4}):
               prices.append(price.text)
          for change in listing.find_all('td', attrs={'data-reactid':40+5}):
               changes.append(change.text)
          for percentChange in listing.find_all('td', attrs={'data-reactid':40+7}):
               percentChanges.append(percentChange.text)
     # print(pd.DataFrame({"Names": names, "Prices": prices, "Change": changes, "% Change": percentChanges}))
     return(prices[0])

def get_nifty_sensex():
     WorldIndicesUrl = "https://in.finance.yahoo.com/world-indices"
     r= requests.get(WorldIndicesUrl)
     data=r.text
     soup=BeautifulSoup(data,features="html.parser")

     i_prices=[]
     i_names=[]
     for row in soup.find_all('tbody'):
          for srow in row.find_all('tr'):
               for name in srow.find_all('td', attrs={'class':'data-col1'}):
                    i_names.append(name.text)
               for price in srow.find_all('td', attrs={'class':'data-col2'}):
                    i_prices.append(price.text)    
     
     print(pd.DataFrame({"Names": i_names, "Prices": i_prices}))
     return([i_prices[0],i_prices[1]])


@app.route('/', methods=['GET'])
def index1():
     return(render_template("index.html"))
    
@app.route('/data',methods=['GET'])
def data():
     print("here")
     usd=get_usd()
     nifty_sensex=get_nifty_sensex()
     print([usd,nifty_sensex[0],nifty_sensex[1]])
     return(jsonify({'nifty':nifty_sensex[1],
     'sensex':nifty_sensex[0],
     'usd':usd} ))

@app.route('/static/stock1',methods=['GET'])
def stock1():

     df=pd.read_csv("FB.csv")
     dates=[]
     

     df_date=df.loc[:,'Date']
     df_close=df.loc[:,'Close']
     df['Date'] = pd.to_datetime(df['Date'])
     df_date_pred=df.loc[:,'Date']
     for date in df_date_pred:
          dates.append(date.toordinal())
     df_date=list(df_date)
     df_date.append('2020-05-01')
     df_close=list(df_close)
     max_price=max(df_close)
     min_price=min(df_close)
     
     
     dates=np.array(dates)
     dates=dates.reshape(-1,1)
     dates_test=[dates[-1]+30]


     svr_lin=SVR(kernel='rbf',degree=10,C=1e3)
     svr_lin.fit(dates,df_close)
     predictions=svr_lin.predict(dates_test)
     print(predictions)
     pred_price=predictions[-1]
     for i in predictions:
          df_close.append(i)
    
     return(jsonify({'dates':df_date,
     'close':df_close,
     'max_price':round(max_price,5),
     'min_price':round(min_price,5),
     'pred_price':round(pred_price,5)}  ))



@app.route('/static/stock2',methods=['GET'])
def stock2():
     df=pd.read_csv("MSFT.csv")
     dates=[]
     

     df_date=df.loc[:,'Date']
     df_close=df.loc[:,'Close']
     df['Date'] = pd.to_datetime(df['Date'])
     df_date_pred=df.loc[:,'Date']
     for date in df_date_pred:
          dates.append(date.toordinal())
     df_date=list(df_date)
     df_date.append('2020-05-01')
     df_close=list(df_close)
     max_price=max(df_close)
     min_price=min(df_close)
     
     
     dates=np.array(dates)
     dates=dates.reshape(-1,1)
     dates_test=[dates[-1]+30]


     svr_lin=SVR(kernel='rbf',degree=10,C=1e3)
     svr_lin.fit(dates,df_close)
     predictions=svr_lin.predict(dates_test)
     print(predictions)
     pred_price=predictions[-1]
     for i in predictions:
          df_close.append(i)
    
     return(jsonify({'dates':df_date,
     'close':df_close,
     'max_price':round(max_price,5),
     'min_price':round(min_price,5),
     'pred_price':round(pred_price,5)}  ))

if (__name__=="__main__"):
     app.run()

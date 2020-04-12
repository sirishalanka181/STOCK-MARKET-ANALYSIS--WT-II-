import csv 
import pandas as pd 
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, jsonify
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
     usd=get_usd()
     nifty_sensex=get_nifty_sensex()
     print([usd,nifty_sensex[0],nifty_sensex[1]])
     return(render_template("index.html",usd=usd,sensex=nifty_sensex[0],nifty=nifty_sensex[1]))


if (__name__=="__main__"):
     app.run()

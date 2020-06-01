'''
Created on Jun 28, 2018

@author: CEVDEA
'''

import urllib as u
from bs4 import BeautifulSoup as bs

import os
import openpyxl

import quandl
quandl.ApiConfig.api_key = 'WoNBJsg2b26KEheDJW_t'

import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web2

"""
First visit www.Finviz.com and get the base url for the quote page.
example: http://finviz.com/quote.ashx?t=aapl

Then write a simple function to retrieve the desired ratio. 
In this example I'm grabbing Price-to-Book (mrq) ratio

To complete this I have to:
    1) Access the TKTs that I have defined in the excel sheet
        a) Abrir el archivo de excel
        b) Buscar la hoja donde estan los TKT
        c) crear una lista de los TKT
            i) si estan repetidos ponerle el numero de la columna para poder ubicarlo
    2) Get the current price for them
    3) Decide what to do next 
"""

def get_price2book( symbol ):
    try:
        url = r'http://finviz.com/quote.ashx?t={}'\
                        .format(symbol.lower())
        html = u.request.urlopen(url).read()
        soup = bs(html, 'lxml')
        # Change the text below to get a diff metric
        pb =  soup.find(text = r'P/B')
        pb_ = pb.find_next(class_='snapshot-td2').text
        print( '{} price to book = {}'.format(symbol, pb_) )
        return pb_
    except Exception as e:
        print(e)
        
def get_price( symbol ):
    try:
        url = r'http://finviz.com/quote.ashx?t={}'\
                        .format(symbol.lower())
        html = u.request.urlopen(url).read()
        soup = bs(html, 'lxml')
        # Change the text below to get a diff metric
        pb =  soup.find(text = r'Price')
        pb_ = pb.find_next(class_='snapshot-td2').text
        print( '{} price = {}'.format(symbol, pb_) )
        return pb_
    except Exception as e:
        print(e)
        
"""
Construct a pandas series whose index is the list/array
of stock symbols of interest.

Run a loop assigning the function output to the series
"""
input_dir = r'C:\Users\cevdea\Google Drive\trading\kirk\2019\active trading'
input_file = '20190107_Money Management Spreadsheet.xlsx'
input_sheet = 'TKT_TT'

#Step 01
os.chdir(input_dir)
incident_wb = openpyxl.load_workbook(input_file)
sheet = incident_wb.get_sheet_by_name(input_sheet) 

tkt_list = []

#for row in range(2, sheet.max_row + 1):
for row in range(2, 5):
    print('*')
    tkt = sheet['B' + str(row)].value
    print('*** row *** ' + str(row))
    print(tkt)
    try:
        if tkt is not None:
            if tkt[0] != '$':
                tkt_list.append(tkt)
    except :
        print('failure reading dimension for record ' + str(row))

print(tkt_list)

#stock_list = ['XOM','AMZN','AAPL','SWKS']
stock_list = tkt_list
p2b_series = pd.Series( index=stock_list )

for sym in stock_list:
    p2b_series[sym] = get_price(sym)
    
# get the table for daily stock prices and,
# filter the table for selected tickers, columns within a time range
# set paginate to True because Quandl limits tables API to 10,000 rows per call

data = quandl.get_table('WIKI/PRICES', ticker = ['MSFT'], 
                        qopts = { 'columns': ['ticker', 'date', 'adj_close'] }, 
                        date = { 'gte': '2018-01-01', 'lte': '2018-10-01'  }, 
                        paginate=True)
print(data)


# Other workaround
style.use('ggplot')

start = dt.datetime(2017, 1, 1)
end = dt.datetime.now()

df = web2.DataReader("eric", 'yahoo', start, end)
print(df)
df.reset_index(inplace=True)
df.set_index("Date", inplace=True)

#df = df.drop("Symbol", axis=1)

df['Close'].plot()
plt.legend()
plt.show()


    
print("fin")
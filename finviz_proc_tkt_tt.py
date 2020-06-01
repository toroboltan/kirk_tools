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

print("*** inicio ***")

input_dir = r'C:\Users\cevdea\Google Drive\trading\kirk\2019\active trading'
input_file = '20190107_Money Management Spreadsheet.xlsx'
input_sheet = 'TKT_TT_PY_2019'

#Step 01 - open excel directly
os.chdir(input_dir)
trading_wb = openpyxl.load_workbook(input_file)
trading_sheet = trading_wb.get_sheet_by_name(input_sheet)

#Step 02 - open excel in pandas
df_trading = pd.read_excel(input_file, input_sheet)
print(df_trading.shape)

stock_list = df_trading['TKT'].tolist()
print('stock_list')
print(stock_list)

for sym in stock_list:
    tkt_cell = stock_list.index(sym)
    precio = get_price(sym)
    print('cell: ' + str(tkt_cell+2))
    trading_sheet.cell(row=(tkt_cell+2), column=10).value = precio
    
trading_wb.save(input_file)


print("*** fin ***")
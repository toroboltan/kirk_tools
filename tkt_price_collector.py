'''
Created on Jan 16, 2019

This script:

    A) collects TKTs from the excel workbook, sheet and date indicated as parameters and gets:

        1) Price
        2) SMA 20
        3) SMA 50
        4) SMA 200
        5) Perf Week
        6) Perf Month
        7) Perf Quarter
        8) Perf Half Year
        9) Perf Year
       10) Perf YTD
       
    
    B) saves the information adding the date in a CSV file.
    
    C) in the date is included in the CSV file it does not include it in the file
    
    D) Incorporate a GUI to collect the information related to the parameters
    
    E) Load the output CSV in a database


@author: CEVDEA
'''
import os
import openpyxl

import urllib as u
from bs4 import BeautifulSoup as bs

import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web2


def get_price_parameter(symbol, parameter):
    try:
        url = r'http://finviz.com/quote.ashx?t={}'\
                        .format(symbol.lower())
        html = u.request.urlopen(url).read()
        soup = bs(html, 'lxml')
        # Change the text below to get a diff metric
        pb =  soup.find(text = parameter)
        pb_ = pb.find_next(class_='snapshot-td2').text
        print( '{} price = {}'.format(symbol, pb_) )
        return pb_
    except Exception as e:
        print(e)

def get_tkt_title(symbol):
    try:
        url = r'http://finviz.com/quote.ashx?t={}'\
                        .format(symbol.lower())
        html = u.request.urlopen(url).read()
        soup = bs(html, 'lxml')
        # Change the text below to get a diff metric
        pb =  soup.title.string
        return pb
    except Exception as e:
        print(e)

input_dir = r'C:\Users\cevdea\Google Drive\trading\kirk\2019\Listas'
input_file = 'ETF_TKT.xlsx'
input_sheet = 'ETF'
column_tkt = 'TKT'
column_seg = 'Segment'

parameters_list = [r'Price',
                   r'SMA20',
                   r'SMA50',
                   r'SMA200',
                   r'Perf Week',
                   r'Perf Month',
                   r'Perf Quarter',
                   r'Perf Half Y',
                   r'Perf Year',
                   r'Perf YTD']


print("*** inicio ***")

#Step 01 - open excel directly
os.chdir(input_dir)
trading_wb = openpyxl.load_workbook(input_file)
trading_sheet = trading_wb.get_sheet_by_name(input_sheet)

#Step 02 - open excel in pandas
df_trading = pd.read_excel(input_file, input_sheet)
print(df_trading.shape)

stock_list = df_trading[column_tkt].tolist()
print('stock_list')
print(stock_list)

for sym in stock_list:
    linea = sym + ',' + get_tkt_title(sym)
    for parameter in parameters_list:
        parameter_value = get_price_parameter(sym, parameter)
        linea = linea + ',' + parameter_value
    print(linea)

print("*** fin ***")


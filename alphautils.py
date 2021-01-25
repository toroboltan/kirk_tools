## Imports
import yfinance as yf
import finviz as fvz
import os
from openpyxl import load_workbook
import pandas as pd
import datetime as dt
import kirkconstants as kc
import updatemms as upm
import tradingutils as trutil
import requests
import numpy as np
import time
import alphakeys as ak


def GetPriceDailyAlpha(symbol, size, apikey):
    function='TIME_SERIES_DAILY_ADJUSTED'
    url = 'https://www.alphavantage.co/query'
    parametros = {'function' : function, 'symbol': symbol, 
                  'outputsize': size, 'apikey': apikey}

    r = requests.get(url, params=parametros)
    data = r.json()['Time Series (Daily)']
    dataDF = pd.DataFrame.from_dict(data, orient='index')
    dataDF = dataDF.astype('float')
    dataDF.index.name = 'Date'
    dataDF.columns = ['Open','High','Low','Close','AdjClose','Volume','Div','Split']
    dataDF = dataDF.sort_values('Date', ascending=True).round(2)
    dataDF.index = pd.to_datetime(dataDF.index)
    return dataDF

def GetMovingAvgAlpha(symbol, interval, series_type, time_period, mean_type, apikey):
    function = mean_type
    url = 'https://www.alphavantage.co/query'
    parametros = {'function':function, 'symbol':symbol, 'interval':interval, 
                  'series_type':series_type,'time_period':time_period ,'apikey':apikey}

    r = requests.get(url, params=parametros)
    js = r.json()['Technical Analysis: '+ mean_type]
    df = pd.DataFrame.from_dict(js, orient='index')
    df = df.astype('float')
    df.index.name = 'Date'
    df = df.sort_values('Date', ascending=True).round(2)
    #additional change
    if (interval == 'daily') or (interval == 'weekly') or (interval == 'monthly'):
        tf = interval[0].upper()
    else:
        tf = interval
    df.columns = [mean_type + '(' + str(time_period) + tf + ')']
    #additional change
    df.index = pd.to_datetime(df.index)
    return df

def GetStochAlpha(symbol, interval, fastkperiod, slowkperiod , slowdperiod, apikey):
    function = 'STOCH'
    url = 'https://www.alphavantage.co/query'
    parametros = {'function':function, 'symbol':symbol, 'interval':interval, 
                  'fastkperiod':fastkperiod, 'slowkperiod':slowkperiod, 'slowdperiod': slowdperiod, 
                  'apikey':apikey}

    r = requests.get(url, params=parametros)
    js = r.json()['Technical Analysis: '+ function]
    df = pd.DataFrame.from_dict(js, orient='index')
    df = df.astype('float')
    df.index.name = 'Date'
    df = df.sort_values('Date', ascending=True).round(2)
    df.index = pd.to_datetime(df.index)
    return df

def FilterDataDatesAlpha(df, dateBeg, dateEnd):
    startDate = dt.datetime.strptime(dateBeg, '%Y-%m-%d')
    endDate = dt.datetime.strptime(dateEnd, '%Y-%m-%d')
    return df.loc[startDate:endDate]

def GetTktDataFilteredAlpha(symbol, startDate, endDate, mykeys):
    # @TODO: parameterize media average to be collected
    size = 'full'
    # getting and filtering
    # price
    apikey = mykeys.GetAlphaKey()
    dataPrice = GetPriceDaily(symbol, size, apikey)
    dataPrice = FilterDataDates(dataPrice, startDate, endDate)
    # EMA5
    apikey = mykeys.GetAlphaKey()
    dataEMA5 = MovingAv(symbol,'daily','close', 5, 'EMA', apikey)
    dataEMA5 = FilterDataDates(dataEMA5, startDate, endDate)
    # EMA13
    apikey = mykeys.GetAlphaKey()
    dataEMA13 = MovingAv(symbol,'daily','close', 13, 'EMA', apikey)
    dataEMA13 = FilterDataDates(dataEMA13, startDate, endDate)
    #SMA20
    apikey = mykeys.GetAlphaKey()
    dataSMA20 = MovingAv(symbol,'daily','close', 20, 'SMA', apikey)
    dataSMA20 = FilterDataDates(dataSMA20, startDate, endDate)
    #STOCH
    apikey = mykeys.GetAlphaKey()
    dataSTOCH = GetStoch(symbol,'daily', 14, 3, 3, apikey)
    dataSTOCH = FilterDataDates(dataSTOCH, startDate, endDate)

    # @TODO: Do all this merging in a loop
    # merging
    dfMerged = pd.merge(dataPrice, dataEMA5, how='inner', left_index=True, right_index=True)
    dfMerged = pd.merge(dfMerged, dataEMA13, how='inner', left_index=True, right_index=True)
    dfMerged = pd.merge(dfMerged, dataSMA20, how='inner', left_index=True, right_index=True)
    dfMerged = pd.merge(dfMerged, dataSTOCH, how='inner', left_index=True, right_index=True)
    
    # return
    return dfMerged

def GetPriceIntradayAlpha(symbol, size, interval ,apikey):
    function='TIME_SERIES_INTRADAY'
    url = 'https://www.alphavantage.co/query'
    parametros = {'function' : function, 'symbol': symbol,
                  'interval' : interval,
                  'outputsize': size, 'apikey': apikey}

    r = requests.get(url, params=parametros)
    data = r.json()['Time Series (' + interval + ')']
    dataDF = pd.DataFrame.from_dict(data, orient='index')
    dataDF = dataDF.astype('float')
    dataDF.index.name = 'Date'
    dataDF.columns = ['Open','High','Low','Close','Volume']
    dataDF = dataDF.sort_values('Date', ascending=True).round(2)
    dataDF.index = pd.to_datetime(dataDF.index)  
    return dataDF

def GetVWAPIntradayAlpha(symbol, interval ,apikey):
    function='VWAP'
    url = 'https://www.alphavantage.co/query'
    parametros = {'function' : function, 'symbol': symbol,
                  'interval' : interval,
                  'apikey': apikey}

    r = requests.get(url, params=parametros)
    data = r.json()['Technical Analysis: VWAP']
    dataDF = pd.DataFrame.from_dict(data, orient='index')
    dataDF = dataDF.astype('float')
    dataDF.index.name = 'Date'
    #dataDF.columns = ['Open','High','Low','Close','Volume']
    dataDF = dataDF.sort_values('Date', ascending=True).round(2)
    dataDF.index = pd.to_datetime(dataDF.index)    
    return dataDF

def GetTkTShortTermInfoAlpha(tkt, mykeys):
    apikey = mykeys.GetAlphaKey()
    df_p = GetPriceIntraday('SPY', 'full', '30min', apikey)
    apikey = mykeys.GetAlphaKey()
    df_vw = GetVWAPIntraday('SPY', '30min', apikey)
    dfMerged = pd.merge(df_p, df_vw, how='inner', left_index=True, right_index=True)
    return dfMerged

def TestAlphaUtils():
    print('*** Begin - TestAlphaUtils ***')
    dateBeg = '2015-01-01'
    dateEnd = '2020-09-21'
    
    # Formatting pandas to have 2 decimal points
    pd.options.display.float_format = "{:,.2f}".format
    
    # Alphavantage Keys
    mykeys = ak.alphaKeys()
 
    # Time Conversion
    startDate = dt.datetime.strptime(dateBeg, '%Y-%m-%d')
    endDate = dt.datetime.strptime(dateEnd, '%Y-%m-%d')
 
    print('*** End - TestAlphaUtils ***')

def main():
    TestAlphaUtils()

if __name__ == "__main__":
    try:
        main()
    except SystemExit as e:
        print('Error Exception triggered')

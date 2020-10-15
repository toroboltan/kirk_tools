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

## Constants
CASH = 'cash'

## Testing data
lst_market = ['SPY', 'QQQ', 'DIA', 'IWM']
start_date = '2019-10-12'
end_date = '2020-10-12'
format_date = '%Y-%m-%dT%T-06:00'

def GetAccount(api_key, secret_key):    
    
    headers ={"APCA-API-KEY-ID" : api_key, "APCA-API-SECRET-KEY":secret_key}
    endpoint = "https://paper-api.alpaca.markets/v2/account"
    
    r = requests.get(url = endpoint, headers = headers)
    
    js = r.json()
    return js

def GetHistory(symbol, start_date, end_date, api_key, secret_key, timeframe='1D'):    
    
    start = dt.datetime.strftime(start_date, format=format_date)
    end = dt.datetime.strftime(end_date, format=format_date)

    headers ={"APCA-API-KEY-ID" : api_key, "APCA-API-SECRET-KEY":secret_key}
    params =  {'symbols' : symbol, 'start':start, 'end':end}
    endpoint = "https://data.alpaca.markets/v1/bars/"+timeframe
    
    r = requests.get(url = endpoint, headers =headers, params=params)
    
    js = r.json()
    
    tickers = symbol.split(",")
    dfs = {}
    for ticker in tickers:
        dfs[ticker] = pd.DataFrame(js[ticker])
        dfs[ticker].t = pd.to_datetime(dfs[ticker].t, unit='s')
    return dfs

def FormatDateAndTktList(tkt_list, start_date, end_date):
    str_market = ','.join(lst_market)
    startDate = dt.datetime.strptime(start_date, '%Y-%m-%d')
    endDate = dt.datetime.strptime(end_date, '%Y-%m-%d')
    return(str_market, startDate, endDate)

def PrintKeys(apiKey, secretKey):
    print('apiKey: ' + apiKey)
    print('secretKey: ' + secretKey)

def PrintAccount(apiKey, secretKey):
    js_account = GetAccount(apiKey, secretKey)
    print('account: ' + js_account.get(CASH))

def PrintMarketData(lst_market, start_date, end_date, apiKey, secretKey, tframe):
    str_market, startDate, endDate = FormatDateAndTktList(lst_market, start_date, end_date)
    dfs = GetHistory(str_market, startDate, endDate, apiKey, secretKey, timeframe=tframe)
    print(dfs['SPY'])

def PrintMarketData30Min(lst_market, start_date, end_date, apiKey, secretKey):
    str_market, startDate, endDate = FormatDateAndTktList(lst_market, start_date, end_date)
    dfs = GetHistory(str_market, startDate, endDate, apiKey, secretKey, timeframe='day')
    print(dfs['SPY'])

def main():
    # Setting Keys
    apiKey = kc.ALPACA_API_KEY
    secretKey = kc.ALPACA_SECRET_KEY
    tframe1d = 'day'
    tframe15m = '15min'
    # Testing
    PrintKeys(apiKey, secretKey)
    PrintAccount(apiKey, secretKey)
    PrintMarketData(lst_market, start_date, end_date, apiKey, secretKey, tframe1d)
    #PrintMarketData(lst_market, start_date, end_date, apiKey, secretKey, tframe15m)

if __name__ == "__main__":
    try:
        main()
    except SystemExit as e:
        print('Error Exception triggered')
import requests
import pandas as pd
import numpy as np 
import updatemms as upm
import kirkconstants as kc
import pickle
import tqdm
import os
import sys
import finviz
import dbhandler as dbh
import yfinance as yf
import datetime
import tqdm, sys, time, threading

'''
    Steps:
        1) Load playbook in pandas from excel
           - Limit dates to a specific year
        2) Update prices
           - Read values from finviz 
           - Read values from Alpaca (just need closing price)
        3) Implement formulas defined in Excel based on target
'''

# Constants - Candidates Table fields
source = 'source'	
date = 'date'
tkt = 'tkt'	
tkt_name = 	'tkt_name'
yf_info = 'yf_info'
tkt_type = 'tkt_type'
tf = 'timeframe'
p1 = 'pat_01'
p2 = 'pat_02'
p3 = 'pat_03'
p4 = 'pat_04'
p5 = 'pat_05'
actual_price =	'msft_price'	
init_price = 'init_price'
t1 = 't1'
t2 = 't2'
t3 = 't3'
t4 = 't4'
t5 = 't5'
p1 = 'p1'
p2 = 'p2'
p3 = 'p3'
p4 = 'p4'
p5 = 'p5'	
initial = 'initial_trade_type'	
long_above = 'long_above'	
short_below = 'short_below'
action = 'action_trade_type'
chart_file = 'chart_file'
dir_long = 'Long'
dir_short = 'Short'
act_buy = "BUY"
act_sell = "SELL"
act_neutral = "NEUTRAL"

query_change_type_cand = "ALTER TABLE `tkt_candidates` CHANGE `cand_id` `cand_id` INT(20) NULL DEFAULT NULL;"
query_add_pkey_cand = "ALTER TABLE `tkt_candidates` ADD PRIMARY KEY(`cand_id`);"

def UpdatePlaybookPrices(sql_conn, df):
    notFoundTkt = []
    with tqdm.tqdm(total=len(df), file=sys.stdout) as pbar:
        for idx, row in df.iterrows():
            try:
                df.loc[idx, actual_price] = float(finviz.get_stock(row[tkt])['Price'])
            except:
                print('passed ' + row[tkt])
                notFoundTkt.append(row[tkt])
                pass
            pbar.update()
    print('tkt not found in finviz: ' + str(notFoundTkt))
    #WriteSerialEtfScreen(df, kc.fileNamePickle, kc.testPath)
    print('serial output finished')
    dbh.WriteSQLTable(df, sql_conn, kc.db_table_cand)
    dbh.AlterSQLTable(sql_conn, query_change_type_cand)
    dbh.AlterSQLTable(sql_conn, query_add_pkey_cand)
    print('DB output finished')
    return df

def FormatDataframeYf(df_data, list_tkt):
    '''
        This function formats the dataframe with the following layout
        Date - Close - High - Low - Open - symbol ...
    '''
    tktLabel = 'symbol'
    index_name = 0
    list_df = []
    with tqdm.tqdm(total=len(list_tkt), file=sys.stdout) as pbar:
        for tkt in list_tkt:
            pbar.update()
            list_item = df_data[tkt].head(1).copy() #copy only first element
            list_item[tktLabel] = tkt
            list_df.append(list_item)
    total_df = pd.concat(list_df)
    total_df.columns = total_df.columns.str.lower()
    total_df.rename(columns = {'symbol':'tkt'}, inplace= True)     
    return(total_df)

def GetCurrentPriceYf(tktList, start_date, end_date, interval):
    ''' 
        This function receives a list of tkts and returns a pandas 
        with the current associated data
    '''
    tkt_df = yf.download(tktList, start=start_date, end=end_date, interval=interval, auto_adjust=True)
    tkt_df = tkt_df.swaplevel(i=1, j=0, axis=1)
    return FormatDataframeYf(tkt_df, tktList)

def GetSinglePriceYf(tkt_var, start_date, end_date, interval):
    ''' 
        This function receives a list of tkts and returns a pandas 
        with the current associated data
    '''
    close_price = 'Close'
    tkt_df = yf.download(tkt_var, start=start_date, end=end_date, interval=interval, auto_adjust=True)
    return tkt_df[close_price].iloc[0]

def ReadExcelPlaybook():
    ''' 
        This function reads the excel with the candidates and returns
        a dataframe
    '''
    pbPath = kc.pbPath
    pbFile = kc.pbFile
    pbSheet = kc.pbSheet
    df = upm.OpenExcelFile(pbPath, pbFile, pbSheet)
    return df

def UpdatePlaybookNames(df):
    ''' 
        This function adds tkt names to playbook dataframe
    '''
    shortName = 'shortName'
    notFoundTkt = []
    with tqdm.tqdm(total=len(df), file=sys.stdout) as pbar:
        for idx, row in df.iterrows():
            try:
                #df.loc[idx, tkt_name] = yf.Ticker(df.loc[idx, tkt]).info['shortName']
                df.loc[idx, yf_info] = yf.Ticker(df.loc[idx, tkt])
            except:
                print('failed ' + row[tkt])
                notFoundTkt.append(row[tkt])
                pass
            pbar.update()
    print('test_yer')
    '''
    with tqdm.tqdm(total=len(df), file=sys.stdout) as pbar:
        for idx, row in df.iterrows():
            try:
                df.loc[idx, tkt_name] = df.loc[idx, yf_info].info['longName']
            except:
                print('failed ' + row[tkt])
                notFoundTkt.append(row[tkt])
                pass
            pbar.update()
        df[tkt_name] = df[yf_info].info['longName']
    '''
    print('tkt not found in yfinance: ' + str(notFoundTkt))
    return df

def UpdatePlaybookPricesTest(df):
    ''' 
        This function update prices to playbook dataframe
    '''
    notFoundTkt = []
    interval = '1d'
    currDate = datetime.date.today()
    with tqdm.tqdm(total=len(df), file=sys.stdout) as pbar:
        for idx, row in df.iterrows():
            try:
                df.loc[idx, actual_price] = GetSinglePriceYf(df.loc[idx, tkt], currDate, None, interval)
            except:
                print('failed ' + row[tkt])
                notFoundTkt.append(row[tkt])
                pass
            pbar.update()
    print('test_yer')
    print('tkt not found in yfinance: ' + str(notFoundTkt))
    return df


def Unique(list1):
    '''
        function returns a list of unique elements
        from list1 
    '''
    x = np.array(list1)
    return np.unique(x).tolist()

def main(arg):
    sql_conn = dbh.ConnectSQLDb(kc.db_prefix, kc.db_struc_etf)
    # Formatting pandas to have 2 decimal points
    pd.options.display.float_format = "{:,.2f}".format
    print('___Begin main()___')
    if arg == 'test01':
        print('test 01')
        df_price = ReadExcelPlaybook()
        df_price = UpdatePlaybookPrices(sql_conn, df_price)
    
    if arg == 'test02':
        # This is a test to collect daily prices 
        print('test 02')
        tktJeroCand = ['SPY', 'QQQ', 'IWM', 'DIA']
        interval = '1d'
        currDate = datetime.date.today()
        prevDate = datetime.date.today() - datetime.timedelta(1)
        final_df = GetCurrentPriceYf(tktJeroCand, currDate, None, interval)
        for tkt in tktJeroCand:
            print('TKT: ' + tkt + ' closing price: ' + str(final_df[final_df['symbol'] == tkt]['Close'].iloc[0]))
        print('end')
    
    if arg == 'test03':
        # This is a test to open the candidates file
        print('test 03')
        df_pb = ReadExcelPlaybook()
        df_pb = UpdatePlaybookNames(df_pb)
        print('end test 03')

    if arg == 'test04':
        print('test04')
        # This is a test to open the candidates file
        df_pb = ReadExcelPlaybook()
        df_pb = UpdatePlaybookPricesTest(df_pb)
        print('end test 04')

    if arg == 'test05':
        # This is a test to collect daily prices 
        print('test 05')
        tktJeroCand = 'AMZN'
        interval = '1d'
        currDate = datetime.date.today()
        final_price = GetSinglePriceYf(tktJeroCand, currDate, None, interval)
        print('TKT: ' + tktJeroCand + ' closing price: ' + str(final_price))
        print('end test 05')

    if arg == 'test06':
        print('test06')
        # This is a test to open the candidates file
        tkt = 'tkt'
        df_pb = ReadExcelPlaybook()
        list_tkt = Unique(df_pb['tkt'].values.tolist())
        currDate = '2020-12-24'
        interval = '1d'
        df_prices = GetCurrentPriceYf(list_tkt, currDate, None, interval)
        df_merge = pd.merge(df_pb, df_prices, how= 'left', on= 'tkt')
        df_merge.dropna(subset = ['close'], inplace= True)
        print('end test 06')

    print('___End main()___')

if __name__ == "__main__":
    arg = 'test06'
    try:
        main(arg)
    except SystemExit as e:
        print('Error Exception triggered')
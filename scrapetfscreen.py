import requests
import pandas as pd
import updatemms as upm
import kirkconstants as kc
import pickle
import tqdm
import os
import sys
import finviz
from sqlalchemy import create_engine

url_etf = f'https://www.etfscreen.com/performance.php?wl=0&s=Rtn-1d%7Cdesc&t=6&d=i&ftS=yes&ftL=no&vFf=dolVol21&vFl=gt&vFv=100000&udc=default&d=i'

header_etf = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"
}

index_etf = 2

def ToNumeric(df, columns):
    for col in columns:
        count_T, count_B, count_M, count_K = 0,0,0,0
        for idx, row in df.iterrows():
            try:
                tril = (row[col]).upper().find('T') 
                bill = (row[col]).upper().find('B') 
                mill = (row[col]).upper().find('M')
                thou = (row[col]).upper().find('K')
                if  tril > 0:
                    count_T += 1
                    df.loc[idx, col] = float(row[col][:tril]) * 10**12
                elif  bill > 0:
                    count_B += 1
                    df.loc[idx, col] = float(row[col][:bill]) * 10**9
                elif  mill > 0:
                    count_M += 1
                    df.loc[idx, col] = float(row[col][:mill]) * 10**6
                elif  thou > 0:
                    count_K += 1
                    df.loc[idx, col] = float(row[col][:thou]) * 10**3
            except:
                pass
        print(f'column: {col}, T->{count_T}, B->{count_B}, M->{count_M}, K->{count_K}')

def ToFloat(df, columns):
    for col in columns:
        df[col] = df[col].astype(float)

def ReadEtfScreen(url, header, indexetf):
    r = requests.get(url, headers=header)
    tables = pd.read_html(r.text)
    return tables[indexetf]

def FormatEtfScreen(df):
    # Drop first row
    df.drop(0 ,axis=0 ,inplace=True)
    # Drop first collum
    df.drop('✓', axis=1, inplace=True)
    # Format column names
    oldColNames_lst = df.columns.to_list()
    newColNames_lst = [x.lower() for x in oldColNames_lst]
    newColNames_lst = [x.replace('-','_') for x in list(newColNames_lst)]
    newColNames_lst = [x.replace('$','') for x in list(newColNames_lst)]
    df.columns = newColNames_lst
    ToNumeric(df, ['vol_21'])
    ToFloat(df, ['vol_21'])
    return df

def WriteSerialEtfScreen(data, file_name, script_path):
    os.chdir(script_path)
    with open(file_name, 'wb') as f:
        pickle.dump(data, f)

def ReadSerialEtfScreen(file_name, script_path):
    os.chdir(script_path)
    # open a file, where you stored the pickled data
    f = open(file_name, 'rb')
    # dump information to that file
    data = pickle.load(f)
    # close the file
    f.close()
    return data

def TestCase01():
    ''' Read data from etfscreen.com '''
    etf_df = ReadEtfScreen(url_etf, header_etf, index_etf)
    WriteSerialEtfScreen(etf_df, kc.fileNamePickle, kc.testPath)
    return etf_df

def TestCase02():
    ''' Format data from etfscreen.com and stores it into SQL db '''
    etf_df = ReadSerialEtfScreen(kc.fileNamePickle, kc.testPath)
    etf_df = FormatEtfScreen(etf_df)
    sql_conn = ConnectSQLDb(kc.db_prefix, kc.db_struc_etf)
    etf_df.to_sql(con=sql_conn, name=kc.db_table_etf, if_exists='replace')
    return etf_df

def ConnectSQLDb(db_prefix ,db_struct):
    ''' Connect to SQL database '''
    #Seteo el USER : PASS @ HOST / BBDD_NAME
    #sql_engine = create_engine('mysql+pymysql://root:@localhost/etfscreendb')
    sql_engine = create_engine(db_prefix + db_struct)
    sql_conn = sql_engine.connect()
    return sql_conn

def ProcessEtfscreen():
    ''' Read data from etfscreen.com 
        Format data from etfscreen.com and stores it into SQL db '''   
    etf_df = TestCase01()
    etf_df = TestCase02()
    etf_df = AddPriceEtfScreen()
    return etf_df

def ReadSQLTable(db_prefix ,db_struct, db_table):
    ''' Read data from SQL db and returns pandas df '''
    sql_conn = ConnectSQLDb(db_prefix, db_struct)
    data_df = pd.read_sql(db_table, con=sql_conn)
    return data_df

def WriteSQLTable(df, db_prefix ,db_struct, db_table):
    ''' Read data from SQL db and returns pandas df '''
    sql_conn = ConnectSQLDb(db_prefix, db_struct)
    df.to_sql(con=sql_conn, name=db_table, if_exists='replace')

def AddPriceEtfScreen():
    df = ReadSQLTable(kc.db_prefix, kc.db_struc_etf, kc.db_table_etf)
    with tqdm.tqdm(total=len(df), file=sys.stdout) as pbar:
        for idx, row in df.iterrows():
            try:
                df.loc[idx, 'price'] = float(finviz.get_stock(row['symbol'])['Price'])
            except:
                print('passed ' + row['symbol'])
                pass
            pbar.update()
    WriteSerialEtfScreen(df, kc.fileNamePickle, kc.testPath)
    WriteSQLTable(df, kc.db_prefix ,kc.db_struc_etf, kc.db_table_etf)
    print('AddPriceEtfScreen')
    return df

def EtfPrintTopBottom(tkt_dataframe, numberToPrintInt, timeRange):
    #     name symbol    rsf  rtn_1d  rtn_5d  rtn_1mo  rtn_3mo  rtn_6mo  rtn_1yr       vol_21  price
    lenTktList = len(tkt_dataframe.index)
    if(lenTktList > 0) and (lenTktList >= numberToPrintInt) and (numberToPrintInt):
        final_up_df = pd.DataFrame()
        final_dw_df = pd.DataFrame()
        columnVal = ''
        if timeRange == '1D':
            final_up_df = tkt_dataframe[tkt_dataframe['rtn_1d'] > 0.0].sort_values(by=['rtn_1d'], ascending = False)
            final_dw_df = tkt_dataframe[tkt_dataframe['rtn_1d'] <= 0.0].sort_values(by=['rtn_1d'], ascending = True)
            columnVal = 'rtn_1d'
        if timeRange == '1W':
            final_up_df = tkt_dataframe[tkt_dataframe['rtn_5d'] > 0.0].sort_values(by=['rtn_5d'], ascending = False)
            final_dw_df = tkt_dataframe[tkt_dataframe['rtn_5d'] <= 0.0].sort_values(by=['rtn_5d'], ascending = True)
            columnVal = 'rtn_5d'
        if timeRange == '1M':
            final_up_df = tkt_dataframe[tkt_dataframe['rtn_1mo'] > 0.0].sort_values(by=['rtn_1mo'], ascending = False)
            final_dw_df = tkt_dataframe[tkt_dataframe['rtn_1mo'] <= 0.0].sort_values(by=['rtn_1mo'], ascending = True)
            columnVal = 'rtn_1mo'
        if timeRange == '1Q':
            final_up_df = tkt_dataframe[tkt_dataframe['rtn_3mo'] > 0.0].sort_values(by=['rtn_3mo'], ascending = False)
            final_dw_df = tkt_dataframe[tkt_dataframe['rtn_3mo'] <= 0.0].sort_values(by=['rtn_3mo'], ascending = True)
            columnVal = 'rtn_3mo'
        if timeRange == '1H':
            final_up_df = tkt_dataframe[tkt_dataframe['rtn_6mo'] > 0.0].sort_values(by=['rtn_6mo'], ascending = False)
            final_dw_df = tkt_dataframe[tkt_dataframe['rtn_6mo'] <= 0.0].sort_values(by=['rtn_6mo'], ascending = True)
            columnVal = 'rtn_6mo'
        if timeRange == '1Y':
            final_up_df = tkt_dataframe[tkt_dataframe['rtn_1yr'] > 0.0].sort_values(by=['rtn_1yr'], ascending = False)
            final_dw_df = tkt_dataframe[tkt_dataframe['rtn_1yr'] <= 0.0].sort_values(by=['rtn_1yr'], ascending = True)
            columnVal = 'rtn_1yr'
        # Print to the console
        tkts_str =''
        etfStartLine = '*** Print ETF UP - ' + timeRange + ' - (' + str(numberToPrintInt) + ') ***'
        print(etfStartLine)
        for row in final_up_df.head(numberToPrintInt).iterrows():
            etfLine = row[1]['symbol'] + '\t' + row[1]['name'] + '\t' + str(row[1]['price']) + '\t' + str(row[1][columnVal])
            print(etfLine)
            tkts_str = tkts_str + row[1]['symbol'] + ','
        etfFinalLineUp = "https://www.finviz.com/screener.ashx?v=351&ft=4&t=" + tkts_str[:(len(tkts_str)-1)] + "&o=-change"
        print("tkts_up_str = " + etfFinalLineUp)

        tkts_str =''
        etfStartLine = '*** Print ETF DOWN - ' + timeRange + ' - (' + str(numberToPrintInt) + ') ***'
        print(etfStartLine)    
        for row in final_dw_df.head(numberToPrintInt).iterrows():
            etfLine = row[1]['symbol'] + '\t' + row[1]['name'] + '\t' + str(row[1]['price']) + '\t' + str(row[1][columnVal])
            print(etfLine)
            tkts_str = tkts_str + row[1]['symbol'] + ','
        etfFinalLineDown = "https://www.finviz.com/screener.ashx?v=351&ft=4&t=" + tkts_str[:(len(tkts_str)-1)] + "&o=-change"
        print("tkts_down_str = " + etfFinalLineDown)
        return(etfFinalLineUp, etfFinalLineDown)


def main(arg):
    # Formatting pandas to have 2 decimal points
    pd.options.display.float_format = "{:,.2f}".format
    print('___Begin main()___')
    if arg == 'test01':
        print('test 01')
        etf_df = TestCase01()
    if arg == 'test02':
        print('test 02')
        etf_df = TestCase02()
    if arg == 'test03':
        print('test 03')
        etf_df = ProcessEtfscreen()
    if arg == 'test04':
        print('test04')
        AddPriceEtfScreen()
    print('___End main()___')

if __name__ == "__main__":
    arg = 'test04'
    try:
        main(arg)
    except SystemExit as e:
        print('Error Exception triggered')
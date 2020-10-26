import requests
import pandas as pd
import updatemms as upm
import kirkconstants as kc
import pickle
import os
import sys
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
    etf_df = ReadEtfScreen(url_etf, header_etf, index_etf)
    WriteSerialEtfScreen(etf_df, kc.fileNamePickle, kc.testPath)
    return etf_df

def TestCase02():
    etf_df = ReadSerialEtfScreen(kc.fileNamePickle, kc.testPath)
    etf_df = FormatEtfScreen(etf_df)
    #Seteo el USER : PASS @ HOST / BBDD_NAME
    sql_engine = create_engine('mysql+pymysql://root:@localhost/etfscreendb')
    sql_conn = sql_engine.connect()
    etf_df.to_sql(con=sql_conn, name='etfscreen', if_exists='replace')
    return etf_df

def ProcessEtfscreen():
    etf_df = TestCase01()
    etf_df = TestCase02()
    return etf_df    

def main(arg):
    # Formatting pandas to have 2 decimal points
    pd.options.display.float_format = "{:,.2f}".format
    print('___Begin main()___')
    if arg == 'test01':
        print('test 01')
        etf_df = TestCas01()
    if arg == 'test02':
        print('test 02')
        etf_df = TestCase02()
    if arg == 'test03':
        print('test 03')
        etf_df = ProcessEtfscreen()
    print('___End main()___')

if __name__ == "__main__":
    arg = 'test03'
    try:
        main(arg)
    except SystemExit as e:
        print('Error Exception triggered')
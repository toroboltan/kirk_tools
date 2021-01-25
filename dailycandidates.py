import requests
import pandas as pd
import kirkconstants as kc
import dbhandler as dbh
import updatemms as up
import numpy as np
import datetime

'''
This module takes care of the daily candidates that I collect
after looking at the charts daily.

It has several functions that:

1) Save candidates in a new position in an excel file
2) Save the daily candidates in the database

'''

# Excel info
dcPath= kc.dcPath
dcFile= kc.dcFile
dcSheet= kc.dcSheet
cands = 'NIU,BAC,XOP,REAL,CHAU,PINS,XLE,XLB,MDY,IWC,SHAK,F,MOV,MIK,TNA,DQ,AMZA,XLY,EEM,QCLN,ARKW,IYT,IJS,PRN,QTRX,CORN,BLDP,BNTX,URTY,ACES,UPWK,SPHB,KOD,DUDE,PRVB,ONLN,RTH,LIT,XLF,IEZ,PBW,ETSY,DBC,FTNT,DIA,ROKU,IWM,XES,FCG,POLA,USO,FUTU,FVRR,EH,INTZ,MRUS,OIH,CVNA,GM,MJ,IBUY,CYBR,IYZ,WMT'


def TktsCandToExcel(file_path, file_name, file_sheet, candidates):
    ''' 
    Open de excel file referenced by the variables into a data frame
    and add a new entry with current date, in format yyyy-mm-dd, 
    and candidadates selected 
    '''
    print('TktsCandToExcel - beg')
    df_cand = up.OpenExcelFile(file_path, file_name, file_sheet)
    dateToUse = datetime.date.today()
    df_cand.loc[len(df_cand)] = [np.datetime64(dateToUse), candidates]
    up.SaveExcelFile(df_cand, file_path, file_name, file_sheet)
    print('TktsCandToExcel - end')

def ExcelCandToDb(file_path, file_name, file_sheet, sql_conn, db_table):
    ''' 
    This function loads what it is in the sheet as excel candidates
    and stores it in a SQL db
    '''
    print('ExcelCandToDb - beg')
    df_cand = up.OpenExcelFile(file_path, file_name, file_sheet)
    dbh.WriteSQLTable(df_cand, sql_conn, db_table)
    print('ExcelCandToDb - end')

def AddRowCandToDb(sql_conn, db_table, dateToUse, cands):
    ''' 
    This function adds a row to the database
    '''
    print('AddRowCandToDb - beg')
    row_record = [np.datetime64(dateToUse), cands]
    df_cand = pd.read_sql(db_table, con=sql_conn)
    df_cand.drop(df_cand.columns[0], axis=1, inplace=True)
    df_cand.loc[len(df_cand)] = row_record
    dbh.WriteSQLTable(df_cand, sql_conn, db_table)
    print('AddRowCandToDb - end')

def main(arg):
    # Formatting pandas to have 2 decimal points
    pd.options.display.float_format = "{:,.2f}".format
    print('___Begin main()___')
    if arg == 'test01':
        print('test 01')
        TktsCandToExcel(dcPath, dcFile, dcSheet, cands)
    if arg == 'test02':
        print('test 02')
        db_prefix = kc.db_prefix
        db_struc_etf = kc.db_struc_etf
        db_table = kc.dbCandTable
        sql_conn = dbh.ConnectSQLDb(db_prefix ,db_struc_etf)
        ExcelCandToDb(dcPath, dcFile, dcSheet, sql_conn, db_table)
    if arg == 'test03':
        print('test 03')
        db_prefix = kc.db_prefix
        db_struc_etf = kc.db_struc_etf
        db_table = kc.dbCandTable
        sql_conn = dbh.ConnectSQLDb(db_prefix ,db_struc_etf)
        dateToUse = datetime.date.today()
        AddRowCandToDb(sql_conn, db_table, dateToUse, cands)
    if arg == 'test04':
        print('test04')
    print('___End main()___')

if __name__ == "__main__":
    arg = 'test03'
    try:
        main(arg)
    except SystemExit as e:
        print('Error Exception triggered')
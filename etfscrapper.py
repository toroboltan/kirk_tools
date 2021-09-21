import PySimpleGUI as sg
import os
import sys
import webbrowser
from etfutils import TktScreeenTable
import pandas as pd
import updatemms as up
import tradingutils as tu
import kirkconstants as kc
import scrapetfscreen as scetf
import dbhandler as dbh
import datetime
import dailycandidates as dcan

# Constants

sectorsPerfWindow = (190,28)
                
buttonScrapEtf = 'scrap etfscreen'
buttonReadDb = 'read etfscreendb from db'
buttonReadPicFile = 'read etfscreendb from serial'
buttonWritePicDb = 'write serial to etfscreendb'
buttonExec = 'execute'
buttonConnectDb = 'Conectar DB'


etfPerf1DUp = ""
etfPerf1DDw = ""
etfPerf1WUp = ""
etfPerf1WDw = ""
etfPerf1MUp = ""
etfPerf1MDw = ""
etfPerf1QUp = ""
etfPerf1QDw = ""
etfPerf1HUp = ""
etfPerf1HDw = ""
etfPerf1YUp = ""
etfPerf1YDw = ""

# GUI
sg.theme('BluePurple')

layout = [[sg.Text('*** Conexion DB ***')],
          [sg.Button(buttonConnectDb)], 
          [sg.Text('*** ETF Performance ***')],
          [sg.Button(buttonScrapEtf), 
           sg.Button(buttonReadDb), 
           sg.Button(buttonReadPicFile), 
           sg.Button(buttonWritePicDb),
           sg.Button(buttonExec)], 
          [sg.Text('******************')],         
          [sg.Button('Exit')]]

# Main Program V2

# Open connection to db
window = sg.Window('etfScrapper', layout)
try:
    while True:  # Event Loop
        event, values = window.read()

        if event == 'Exit':
            break
    
        if event == buttonConnectDb:
            sql_conn = dbh.ConnectSQLDb(kc.db_prefix, kc.db_struc_etf)
    
        if event == buttonScrapEtf:
            etf_df = scetf.ProcessEtfscreen(sql_conn)
            if (len(etf_df.index) > 0):
                sg.popup('Message!', 'scrap etfscreen finished!, Click on Execute')
            else:
                sg.popup('Message!', 'etfscreen parsing failed!, Try again in 5 minutes') 
            print('*** ' + event + ' ***')
            print(etf_df)
    
        if event == buttonReadDb:
            etf_df = dbh.ReadSQLTable(sql_conn, kc.db_table_etf)
            print('*** ' + event + ' ***')
            print(etf_df)
    
        if event == buttonReadPicFile:
            etf_df = scetf.ReadSerialEtfScreen(kc.fileNamePickle, kc.testPath)
            print('*** ' + event + ' ***')
            print(etf_df)
    
        if event == buttonWritePicDb:
            etf_df = scetf.ReadSerialEtfScreen(kc.fileNamePickle, kc.testPath)
            dbh.WriteSQLTable(etf_df, sql_conn, kc.db_table_etf)
            print('*** ' + event + ' ***')
            print(etf_df)
    
        if event == buttonExec:
            etf_df = dbh.ReadSQLTable(sql_conn, kc.db_table_etf)
            sg.Print(size=sectorsPerfWindow, do_not_reroute_stdout=False)
            print('*** ETF ***')
            etfPerf1DUp, etfPerf1DDw = scetf.EtfPrintTopBottom(etf_df, kc.topNumber, kc.const1D)
            etfPerf1WUp, etfPerf1WDw = scetf.EtfPrintTopBottom(etf_df, kc.topNumber, kc.const1W)
            etfPerf1MUp, etfPerf1MDw = scetf.EtfPrintTopBottom(etf_df, kc.topNumber, kc.const1M)
            etfPerf1QUp, etfPerf1QDw = scetf.EtfPrintTopBottom(etf_df, kc.topNumber, kc.const1Q)
            etfPerf1HUp, etfPerf1HDw = scetf.EtfPrintTopBottom(etf_df, kc.topNumber, kc.const1H)
            etfPerf1YUp, etfPerf1YDw = scetf.EtfPrintTopBottom(etf_df, kc.topNumber, kc.const1Y)
            sys.stdout = sys.__stdout__
except:
    print('exception generated')
print('last event ' + event)
window.close()
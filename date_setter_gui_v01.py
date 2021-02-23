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

# Functions
def ScreenerArguments(eventPressed): 
    switcher = { 
        'Sectors Daily': [overviewTable, change], 
        'Sectors 1W': [performanceTable, perf1w],
        'Sectors 4W': [performanceTable, perf4w],
        'Sectors 13W': [performanceTable, perf13w],
        'Sectors 26W': [performanceTable, perf26w], 
        'Sectors 52W': [performanceTable, perf52w],
        'Sectors YTD': [performanceTable, perfytd] 
    } 
    # get() method of dictionary data type returns  
    # value of passed argument if it is present  
    # in dictionary otherwise second argument will 
    # be assigned as default value of passed argument 
    return switcher.get(eventPressed, "nothing")

def openweb(browser="", sites=[]):
    if browser == "chrome":
        chromedir= 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
    for site in sites:
        webbrowser.get(chromedir).open(site)

def chartsArgumnets(eventPressed): 
    switcher = {
        'US Markets': etfUsMarkets,
        'Sector ETF': etfSecCht,
        'ETF Perf Daily' : etfPerf1DUp,
        'ETF Perf Weekly' : etfPerf1WUp,       
        'Simple Breakout Scan ETF': etfBrkCht,
        'Simple Breakout Scan STK': stkBrkCht,
        'New High ETF': etfNewHighCht,
        'New High STK': stkNewHighCht,
        'FATGANMSN': fatganmsmCht,
        'Long Breakout Setup ETF': etfLongBrkCht,
        'Long Breakout Setup STK': stkLongBrkCht,
        'Major News': majorNewsCht,
        'Most Shorted Stocks': stkShortSquz,
        'Break Down Setups' : stkShortBrkCht
    }
    # get() method of dictionary data type returns  
    # value of passed argument if it is present  
    # in dictionary otherwise second argument will 
    # be assigned as default value of passed argument 
    return switcher.get(eventPressed, "nothing")

def candList(textTkts):
    return textTkts.replace(" ", "").split(",")

def printBuckets(etfSet, stkSet, listPath, fileList, sheetList):
    # Reading the file
    os.chdir(listPath)
    df = pd.read_excel(fileList, sheet_name=sheetList)
    listBuckets = list(df.columns)
    # Finding buckets for etfs
    tktSetAssigned = set()
    tktSet = etfSet.union(stkSet)
    for bucket in listBuckets:
        print(bucket + ":")
        for tkt in tktSet:
            if (tkt in df[bucket].to_list()):
                print('\t' + tkt)
                tktSetAssigned.add(tkt)
    # Remove from combined set tkts already classified in bucktes
    for tkt in tktSetAssigned:
        tktSet.remove(tkt)
    # Printing Weekly Tkts
    print('Weekly:')
    for tkt in tktSet:
        print('\t' + tkt)

def initializeSets():
    # @TODO: This function has to initialize sets so candidates do not still have stored values for previos iteractions
    print('TODO - initializeSets')

def checkOpenPositions(tktToCheck_lst):
    # @TODO: This function checks if there are candidates with positions already open in the MoneyManagementTable If that is the case they are removed from the list values for previos iteractions 
    print('TODO - checkOpenPositions')   
    return tktToCheck_lst    

listPath = kc.listPath
fileList = kc.fileList
sheetList = kc.sheetList
script_path = kc.script_path
script_list = kc.script_list
tktPath = kc.tktPath

sectorsOverWindow = (157,28)
sectorsPerfWindow = (190,28)
lineStartToChange1 = 'new_date =' 
lineStartToChange2 = 'old_date_header ='
etfPref = "etf"
etfSet = set()
stkSet = set()
list_tktOpen = list()

# Parameters to be used for Performance Table
performanceTable = "Performance"
perf1w = "-perf1w"
perf4w = "-perf4w"
perf13w = "-perf13w"
perf26w = "-perf26w"
perf52w = "-perf52w"
perfytd = "-perfytd"

buttonSecList = ['Sectors Daily',
                 'Sectors 1W',
                 'Sectors 4W',
                 'Sectors 13W',
                 'Sectors 26W',
                 'Sectors 52W',
                 'Sectors YTD']

buttonChtList = ['US Markets',
                 'Sector ETF',
                 'ETF Perf Daily',
                 'ETF Perf Weekly',                 
                 'Simple Breakout Scan STK',
                 'Simple Breakout Scan ETF',
                 'New High STK',
                 'New High ETF',
                 'FATGANMSN',
                 'Long Breakout Setup ETF',
                 'Long Breakout Setup STK',
                 'Major News',
                 'Most Shorted Stocks',
                 'Break Down Setups']
                 
sectorsTktList = ['XLF','EEM','XLE','XLK',
                  'XLV','IYT','XLU','XLI',
                  'XLY','IYR','XLP','XLB',
                  'TLT','GLD','UUP','RTH',
                  'IYZ','SMH','DBC','USO']

textBoxList = ['etfUsMarkets',
               'etfSecCht',
               'etfPerfDaily',
               'etfPerfWeekly',
               'etfBrkCht',
               'stkBrkCht',
               'etfNewHighCht', 
               'stkNewHighCht', 
               'etfLongBrkCht', 
               'stkLongBrkCht', 
               'fatganmsn',
               'majorNewsCht',
               'stkShortSquz',
               'stkShortBrkCht']

buttonProcess = 'Process TKTs'
buttonUpdatePrecios = 'Update Precios'
buttonShowCharts = 'Show Charts'
buttonChkPlaysLong = 'Check Playbook Long'
buttonChkPlaysShort = 'Check Playbook Short'
buttonChkList = 'Check ETFs Lists'
buttonChkMarket = 'Check Market'
buttonScrapEtf = 'scrap etfscreen'
buttonReadDb = 'read etfscreendb from db'
buttonReadPicFile = 'read etfscreendb from serial'
buttonWritePicDb = 'write serial to etfscreendb'
buttonExec = 'execute'
buttonConnectDb = 'Conectar DB'


# Parameters to be used for Overview Table
overviewTable = "Overview"
change = "-change"

# Webpages Links
etfPerLnk = "https://www.etfscreen.com/performance.php?wl=0&s=Rtn-1d%7Cdesc&t=6&d=e&ftS=yes&ftL=no&vFf=dolVol21&vFl=gt&vFv=500000&udc=default&d=i"
etfUsMarkets = "https://www.finviz.com/screener.ashx?v=351&ft=4&t=SPY,IWC,IWM,DIA,OEF,MDY,QQQ&o=-change"
etfSecCht = "https://www.finviz.com/screener.ashx?v=351&ft=4&t=XLF,EEM,XLE,XLK,XLV,IYT,XLU,XLI,XLY,IYR,XLP,XLB,TLT,GLD,UUP,RTH,IYZ,SMH,DBC,USO&o=-change"
etfNewHighCht = "https://www.finviz.com/screener.ashx?v=351&f=ind_exchangetradedfund,sh_avgvol_o100,ta_change_u2,ta_highlow52w_nh&ft=4&o=-change"
stkNewHighCht ="https://www.finviz.com/screener.ashx?v=351&f=ind_stocksonly,sh_avgvol_o100,ta_change_u2,ta_highlow52w_nh&ft=4&o=-change"
fatganmsmCht = "https://www.finviz.com/screener.ashx?v=351&t=FB,AAPL,GOOGL,AMZN,NFLX,MSFT,SBUX,NKE,TSLA&o=-change"
majorNewsCht = "https://www.finviz.com/screener.ashx?v=320&s=n_majornews"

# Scans
etfLongBrkCht = "https://www.finviz.com/screener.ashx?v=351&f=ind_exchangetradedfund,sh_avgvol_o400,sh_price_o5,ta_averagetruerange_o1.5,ta_change_u2,ta_highlow20d_b0to3h,ta_highlow50d_b0to3h,ta_sma20_pa,ta_sma200_pa,ta_sma50_pa&ft=4&o=-change"
stkLongBrkCht = "https://www.finviz.com/screener.ashx?v=351&f=ind_stocksonly,sh_avgvol_o400,sh_price_o5,ta_averagetruerange_o1.5,ta_change_u2,ta_highlow20d_b0to3h,ta_highlow50d_b0to3h,ta_sma20_pa,ta_sma200_pa,ta_sma50_pa&ft=4&o=-change"
stkBrkCht = "https://www.finviz.com/screener.ashx?v=351&f=ind_stocksonly,sh_avgvol_o100,sh_curvol_o500,sh_price_o5,ta_change_u2,ta_changeopen_u3,ta_highlow52w_nh,ta_perf_dup&ft=4&o=-change"
etfBrkCht = "https://www.finviz.com/screener.ashx?v=351&f=ind_exchangetradedfund,sh_avgvol_o100,sh_curvol_o500,sh_price_o5,ta_changeopen_u3,ta_highlow52w_nh,ta_perf_dup&ft=4&o=-change"
stkShortSquz = "https://finviz.com/screener.ashx?v=351&f=ind_stocksonly,sh_avgvol_o50,sh_price_o10,sh_relvol_o1,sh_short_o15,ta_change_u2,ta_changeopen_u2,ta_highlow20d_nh,ta_sma50_sb20&ft=4&ta=0&o=perf4w"
stkShortBrkCht = "https://finviz.com/screener.ashx?v=111&f=cap_mid,sh_avgvol_o1000,sh_price_o7,ta_highlow20d_a0to3h,ta_sma20_pb,ta_sma200_pb,ta_sma50_pb&ft=4&o=-change"

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
tkts_up_str = 'tkts_up_str'
showChartsLnk = "https://www.finviz.com/screener.ashx?v=351&t="

# Constants related to etfperf files
newDate = ''
const1D = '1D'
const1W = '1W'
const1M = '1M'
const1Q = '1Q'
const1H = '1H'
const1Y = '1Y'
midFileName = '_etfperf_'
extFileName = '.txt'
constList = [const1D,
             const1W,
             const1M,
             const1Q,
             const1H,
             const1Y]

# GUI
sg.theme('BluePurple')

layout = [[sg.Text('*** Conexion DB ***')],
          [sg.Button(buttonConnectDb)], 
          [sg.Text('*** Posiciones Abiertas ***')],
          [sg.Button(buttonUpdatePrecios), sg.Button(buttonShowCharts)], 
          [sg.Text('*** Chequeo de Indices ***')],
          [sg.Button(buttonChkMarket)], 
          [sg.Text('*** ETF Performance ***')],
          [sg.Button(buttonScrapEtf), 
           sg.Button(buttonReadDb), 
           sg.Button(buttonReadPicFile), 
           sg.Button(buttonWritePicDb),
           sg.Button(buttonExec)], 
          [sg.Text('*** Sectors Performance ***')], 
          [sg.Button('Sectors Daily'), sg.Button('Sectors 1W'), sg.Button('Sectors 4W'),  
           sg.Button('Sectors 13W'), sg.Button('Sectors 26W'), sg.Button('Sectors 52W'),  
           sg.Button('Sectors YTD')],
          [sg.Text('*** Select TKTs Per Chart ***')],
          [sg.Button('US Markets'), sg.InputText(key='etfUsMarkets'),sg.Button('Sector ETF'), sg.InputText(key='etfSecCht')],
          [sg.Button('ETF Perf Daily'), sg.InputText(key='etfPerfDaily'),sg.Button('ETF Perf Weekly'), sg.InputText(key='etfPerfWeekly')],
          [sg.Button('New High ETF'), sg.InputText(key='etfNewHighCht'),sg.Button('New High STK'), sg.InputText(key='stkNewHighCht')],
          [sg.Button('FATGANMSN'), sg.InputText(key='fatganmsn'), sg.Button('Major News'), sg.InputText(key='majorNewsCht')],
          [sg.Text('*** Scans ***')],
          [sg.Button('Simple Breakout Scan ETF'), sg.InputText(key='etfBrkCht'),sg.Button('Simple Breakout Scan STK'), sg.InputText(key='stkBrkCht')],
          [sg.Button('Long Breakout Setup ETF'), sg.InputText(key='etfLongBrkCht'),sg.Button('Long Breakout Setup STK'), sg.InputText(key='stkLongBrkCht')],
          [sg.Button('Most Shorted Stocks'), sg.InputText(key='stkShortSquz'),sg.Button('Break Down Setups'), sg.InputText(key='stkShortBrkCht')],          
          [sg.Text('*** Assign Bucket ***')],
          [sg.Button(buttonProcess), sg.InputText(key='possibleCand')],
          [sg.Text('*** Generate Candidates ***')],
          [ sg.Button(buttonChkPlaysLong), sg.Button(buttonChkPlaysShort), sg.Button(buttonChkList)],
          [sg.Text('******************')],         
          [sg.Button('Exit')]]

# Main Program V2

# Open connection to db
window = sg.Window('TorolGui', layout)

while True:  # Event Loop
    event, values = window.read()
    print(event, values)
    
    if event in (None, 'Exit'):
        break

    if event == buttonConnectDb:
        sql_conn = dbh.ConnectSQLDb(kc.db_prefix, kc.db_struc_etf)

    if event == buttonChkMarket:
        print('test check market')

    if event == buttonChkList:
        result = 1
        result = tu.CheckEtfsLists(tradeType='Long',tradeFlag='LONG')
        if result == 0:
            print('finished')
    
    if event == buttonChkPlaysLong:
        result = 1
        result = tu.GenerateCandidates(tradeType='long')
        if result == 0:
            print('finished')
    
    if event == buttonChkPlaysShort:
        result = 1
        result = tu.GenerateCandidates(tradeType='short')
        if result == 0:
            print('finished')

    if event == buttonUpdatePrecios:
        list_tktOpen = up.UpdatePrices()
        print(list_tktOpen)
   
    if event == buttonShowCharts:
        if len(list_tktOpen) > 0:
            print(showChartsLnk + str(list_tktOpen))
            delim = ','
            openweb("chrome", [showChartsLnk + delim.join(list_tktOpen)])
        
    if event in buttonChtList:
        openweb("chrome", [chartsArgumnets(event)])

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
            
    if event == 'Execute_to_fix':
        fileinfo = values['-IN-']
        print(type(fileinfo))
        fileinfoList = fileinfo.split("/")
        if len(fileinfoList) > 0:
            newDate = fileinfoList[len(fileinfoList) - 1].split("_")[0]
            print('this is new date')
            print(newDate)

            os.chdir(script_path)
        
            for script_file in script_list:
                print('BEGIN Filename is ' + script_file)
                f = open(script_file,"r")
                lines = f.readlines()
                f.close()
                for i, line in enumerate(lines):
                    if(line.startswith(lineStartToChange1) or line.startswith(lineStartToChange2)):
                        line_list = line.split("=")
                        if line.startswith(lineStartToChange1):
                            print("line 1 before" + line_list[1])
                            newString = newDate
                            olString = line_list[1][4:12]
                            line_list[1] = line_list[1].replace(olString, newString)
                            print("line 1 after" + line_list[1])
                        if line.startswith(lineStartToChange2):
                            newString = newDate[0:4]
                            olString = line_list[2][2:6]
                            line_list[2] = line_list[2].replace(olString, newString)
                        lines[i] =  "=".join(line_list)
                f = open(script_file, "w")
                f.write("".join(lines))
                f.close()
                print('END Filename is ' + script_file)
            
            # Execute the file
            for script_file in script_list:
                os.system('python ' + script_file)

    # Performance printing on Windows
    if (event in buttonSecList):
        paramList = ScreenerArguments(event)
        print(paramList)
        if len(paramList) > 1:
            screenResult = TktScreeenTable(sectorsTktList, paramList[0], paramList[1])
            sg.Print(size=sectorsPerfWindow, do_not_reroute_stdout=False)
            print('*** ' + event.upper()  + ' ***')
            print(' ')
            print(screenResult)
            # set output back to console
            sys.stdout = sys.__stdout__
    else:
        if (event == buttonProcess):
            for textTkts in textBoxList:
                print(textTkts + ': '  + values[textTkts])
                if (len(values[textTkts]) > 0):
                    listCand = candList(values[textTkts])
                    if (len(listCand) > 0):
                        if (textTkts.startswith(etfPref)):
                            etfSet.update(listCand)
                        else:
                            stkSet.update(listCand)
            print("etfSet" + ' ' + str(etfSet))
            print("stkSet" + ' ' + str(stkSet))
            if((len(etfSet) > 0) | (len(stkSet) > 0)):
                totalSet = etfSet.union(stkSet)
                finalCand_lst = checkOpenPositions(list(totalSet))
                candString = ','.join(finalCand_lst)
                window['possibleCand'].update(candString)
                dcan.AddRowCandToDb(sql_conn, kc.dbCandTable, datetime.date.today(), candString)
                print(candString)
            sg.Print(size=sectorsPerfWindow, do_not_reroute_stdout=False)
            print('*** CANDIDATES  ***')
            printBuckets(etfSet, stkSet, listPath, fileList, sheetList)
            # set output back to console
            sys.stdout = sys.__stdout__
            initializeSets()
            
window.close()
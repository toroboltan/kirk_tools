'''
Created on Apr 11, 2020


This window will change the value assigned to new_date and old_date_header in date_setter.py script to the value 
what the user introduces

new_date = r"'20200409'"
old_date_header = "filePrefix = '2020"

and then it will run date_setter.py
''

@author: CEVDEA
'''
import PySimpleGUI as sg
import os
import sys
import webbrowser
from etfutils import TktScreeenTable
import pandas as pd
import updatemms as up
import kirkconstants

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
        'ETF Perf Daily' : etfPerfDaily,
        'ETF Perf Weekly' : etfPerfWeekly,       
        'Simple Breakout Scan ETF': etfBrkCht,
        'Simple Breakout Scan STK': stkBrkCht,
        'New High ETF': etfNewHighCht,
        'New High STK': stkNewHighCht,
        'FATGANMSN': fatganmsmCht,
        'Long Breakout Setup ETF': etfLongBrkCht,
        'Long Breakout Setup STK': stkLongBrkCht,
        'Major News':majorNewsCht
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

listPath = kirkconstants.listPath
fileList = kirkconstants.fileList
sheetList = kirkconstants.sheetList
script_path = kirkconstants.script_path
script_list = kirkconstants.script_list
tktPath = kirkconstants.tktPath

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
                 'Major News']

sectorsTktList = ['IWM','XLF','EEM','XLE','XLK',
                  'XLV','IYT','XLU','XLI','XLY',
                  'XLV','IYT','XLU','XLI','XLY',
                  'IYR','XLP','XLB','TLT','GLD',
                  'IYR','XLP','XLB','TLT','GLD',
                  'UUP','RTH','IYZ','SMH','DBC','USO']

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
               'majorNewsCht']

buttonProcess = 'Process Candidates'
buttonUpdatePrecios = 'Update Precios'
buttonShowCharts = 'Show Charts'


# Parameters to be used for Overview Table
overviewTable = "Overview"
change = "-change"

# Webpages Links
etfPerLnk = "https://www.etfscreen.com/performance.php?wl=0&s=Rtn-1d%7Cdesc&t=6&d=e&ftS=yes&ftL=no&vFf=dolVol21&vFl=gt&vFv=500000&udc=default&d=i"
etfUsMarkets = "https://www.finviz.com/screener.ashx?v=351&ft=4&t=SPY,IWC,IWM,DIA,OEF,MDY,QQQ&o=-change"
etfSecCht = "https://www.finviz.com/screener.ashx?v=351&ft=4&t=IWM,XLF,EEM,XLE,XLK,XLV,IYT,XLU,XLI,XLY,IYR,XLP,XLB,TLT,GLD,UUP,RTH,IYZ,SMH,DBC,USO&o=-change"
stkBrkCht = "https://www.finviz.com/screener.ashx?v=351&f=ind_stocksonly,sh_avgvol_o100,sh_curvol_o500,sh_price_o5,ta_change_u2,ta_changeopen_u3,ta_highlow52w_nh,ta_perf_dup&ft=4&ta=0&o=-change"
etfBrkCht = "https://www.finviz.com/screener.ashx?v=111&f=ind_exchangetradedfund,sh_avgvol_o100,sh_curvol_o500,sh_price_o5,ta_changeopen_u3,ta_highlow52w_nh,ta_perf_dup&ft=4&ta=0&o=-change"
etfNewHighCht = "https://www.finviz.com/screener.ashx?v=351&f=ind_exchangetradedfund,sh_avgvol_o100,ta_change_u2,ta_highlow52w_nh&ft=4&o=-change"
stkNewHighCht ="https://www.finviz.com/screener.ashx?v=351&f=ind_stocksonly,sh_avgvol_o100,ta_change_u2,ta_highlow52w_nh&ft=4&o=-change"
etfLongBrkCht = "https://www.finviz.com/screener.ashx?v=351&f=ind_exchangetradedfund,sh_avgvol_o400,sh_price_o5,ta_averagetruerange_o1.5,ta_change_u2,ta_highlow20d_b0to3h,ta_highlow50d_b0to3h,ta_sma20_pa,ta_sma200_pa,ta_sma50_pa&ft=4&ta=0&o=-change"
stkLongBrkCht = "https://www.finviz.com/screener.ashx?v=351&f=ind_stocksonly,sh_avgvol_o400,sh_price_o5,ta_averagetruerange_o1.5,ta_change_u2,ta_highlow20d_b0to3h,ta_highlow50d_b0to3h,ta_sma20_pa,ta_sma200_pa,ta_sma50_pa&ft=4&ta=0&o=-change"
fatganmsmCht = "https://www.finviz.com/screener.ashx?v=351&t=FB,AAPL,GOOGL,AMZN,NFLX,MSFT,SBUX,NKE,TSLA&o=-change"
majorNewsCht = "https://www.finviz.com/screener.ashx?v=320&s=n_majornews"
etfPerfDaily = ""
etfPerfWeekly = ""
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

layout = [[sg.Text('*** Posiciones Abiertas ***')],
          [sg.Button(buttonUpdatePrecios), sg.Button(buttonShowCharts)], 
          [sg.Text('*** ETF Performance: ***'), sg.Text(size=(40,1), key='-OUTPUT-')],
          [sg.Input(key='-IN-')],
          [sg.Button('Open etfscreen age'), sg.Button('File'), sg.Button('Execute')], 
          [sg.Text('*** Sectors Performance ***')], 
          [sg.Button('Sectors Daily'), sg.Button('Sectors 1W'), sg.Button('Sectors 4W'),  
           sg.Button('Sectors 13W'), sg.Button('Sectors 26W'), sg.Button('Sectors 52W'),  
           sg.Button('Sectors YTD')],
          [sg.Text('*** Charts ***')],
#          [sg.Button('US Markets'),
#           sg.Button('Sector ETF'),
#           sg.Button('ETF Perf Daily'),
#           sg.Button('ETF Perf Weekly'),         
#           sg.Button('Simple Breakout Scan ETF'),
#           sg.Button('Simple Breakout Scan STK'),
#           sg.Button('New High ETF'),
#           sg.Button('New High STK'),
#           sg.Button('Long Breakout Setup ETF'),
#           sg.Button('Long Breakout Setup STK')],
#           sg.Button('FATGANMSN'),
#           sg.Button('Major News')],
          [sg.Text('*** Selected TKTs Per Chart ***')],
          [sg.Button('US Markets'), sg.InputText(key='etfUsMarkets'),sg.Button('Sector ETF'), sg.InputText(key='etfSecCht')],
          [sg.Button('ETF Perf Daily'), sg.InputText(key='etfPerfDaily'),sg.Button('ETF Perf Weekly'), sg.InputText(key='etfPerfWeekly')],
          [sg.Button('Simple Breakout Scan ETF'), sg.InputText(key='etfBrkCht'),sg.Button('Simple Breakout Scan STK'), sg.InputText(key='stkBrkCht')],
          [sg.Button('New High ETF'), sg.InputText(key='etfNewHighCht'),sg.Button('New High STK'), sg.InputText(key='stkNewHighCht')],
          [sg.Button('Long Breakout Setup ETF'), sg.InputText(key='etfLongBrkCht'),sg.Button('Long Breakout Setup STK'), sg.InputText(key='stkLongBrkCht')],
#          [sg.Text('From FATGANMSN :'), sg.InputText(key='fatganmsn'), sg.Text('From Major News :'), sg.InputText(key='majorNewsCht')],
          [sg.Button('FATGANMSN'), sg.InputText(key='fatganmsn'), sg.Button('Major News'), sg.InputText(key='majorNewsCht')],
          [sg.Button(buttonProcess)],
          [sg.Text('******************')],
          [sg.Text('Possible Candidates :'), sg.InputText(key='possibleCand')],          
          [sg.Text('******************')],
          [sg.Button('Exit')]]


# Main Program V2

window = sg.Window('TorolGui', layout)

while True:  # Event Loop
    event, values = window.read()
    print(event, values)
    
    if event in (None, 'Exit'):
        break
    
    if event == buttonUpdatePrecios:
        list_tktOpen = up.UpdatePrices()
        print(list_tktOpen)
    
    if event == buttonShowCharts:
        if len(list_tktOpen) > 0:
            print(showChartsLnk + str(list_tktOpen))
            openweb("chrome", [showChartsLnk + str(list_tktOpen)])
        
    if event == 'Open etfscreen age':
        openweb("chrome", [etfPerLnk])
    
    if event in buttonChtList:
        openweb("chrome", [chartsArgumnets(event)])
    
    if event == 'File':
        fname = sys.argv[1] if len(sys.argv) > 1 else sg.popup_get_file('Document to open', initial_folder=tktPath)
        
        if not fname:
            sg.popup("Cancel", "No filename supplied")
            raise SystemExit("Canceling: no filename supplied")
        else:
            window['-OUTPUT-'].update(fname)
            window['-IN-'].update(fname)
            
    if event == 'Execute':
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
            
            # Print in a window the result from performance files
            os.chdir(tktPath)
            totalLines = ''
            for etfTf in constList:
                etfFileName = newDate + midFileName + etfTf + extFileName
                f = open(etfFileName,"r")
                lines = f.readlines()
                for linea in lines:
                    if ((etfTf == const1D) or (etfTf == const1W)):
                        print(etfTf)
                        if (linea.startswith(tkts_up_str)):
                            print(linea)
                            linea_link = linea.split(' ')[2].rstrip("\n")
                            print(linea_link)
                            if (etfTf == const1D):
                                etfPerfDaily = linea_link
                                print('etfPerfDaily ' + etfPerfDaily)
                            else:
                                etfPerfWeekly = linea_link
                                print('etfPerfWeekly ' + etfPerfWeekly)
                    totalLines += linea
                f.close()
            sg.Print(size=sectorsPerfWindow, do_not_reroute_stdout=False)
            print('*** ETF ***')
            print(totalLines)
            # set output back to console
            sys.stdout = sys.__stdout__
            
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
                print(candString)
            sg.Print(size=sectorsPerfWindow, do_not_reroute_stdout=False)
            print('*** CANDIDATES  ***')
            printBuckets(etfSet, stkSet, listPath, fileList, sheetList)
            # set output back to console
            sys.stdout = sys.__stdout__
            initializeSets()
            
window.close()
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

# Environment variables
script_path = r'C:\EclipseWorkspaces\csse120\kirk_tools'
script_list = ['date_setter.py']
tktPath = r'D:\jeronimo\trading\etf'
sectorsOverWindow = (157,28)
sectorsPerfWindow = (190,28)
lineStartToChange1 = 'new_date =' 
lineStartToChange2 = 'old_date_header ='

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
buttonChtList = ['Sector ETF',
                 'Simple Breakout Scan STK',
                 'Simple Breakout Scan ETF',
                 'New High STK',
                 'New High ETF',
                 'FATMAN',
                 'FAGANMSN',
                 'Long Breakout Setup ETF',
                 'Long Breakout Setup STK']
sectorsTktList = ['IWM','XLF','EEM','XLE','XLK',
                  'XLV','IYT','XLU','XLI','XLY',
                  'XLV','IYT','XLU','XLI','XLY',
                  'IYR','XLP','XLB','TLT','GLD',
                  'IYR','XLP','XLB','TLT','GLD',
                  'UUP','RTH','IYZ','SMH','DBC','USO']

# Parameters to be used for Overview Table
overviewTable = "Overview"
change = "-change"

# Webpages Links
etfPerLnk = "https://www.etfscreen.com/performance.php?wl=0&s=Rtn-1d%7Cdesc&t=6&d=i&ftS=yes&ftL=no&vFf=dolVol21&vFl=gt&vFv=500000&udc=default&d=e"
etfSecCht = "https://www.finviz.com/screener.ashx?v=351&ft=4&t=IWM,XLF,EEM,XLE,XLK,XLV,IYT,XLU,XLI,XLY,IYR,XLP,XLB,TLT,GLD,UUP,RTH,IYZ,SMH,DBC,USO&o=-change"
stkBrkCht = "https://www.finviz.com/screener.ashx?v=351&f=ind_stocksonly,sh_avgvol_o100,sh_curvol_o500,sh_price_o5,ta_change_u2,ta_changeopen_u3,ta_highlow52w_nh,ta_perf_dup&ft=4&ta=0&o=-change"
etfBrkCht = "https://www.finviz.com/screener.ashx?v=111&f=ind_exchangetradedfund,sh_avgvol_o100,sh_curvol_o500,sh_price_o5,ta_changeopen_u3,ta_highlow52w_nh,ta_perf_dup&ft=4&ta=0&o=-change"
etfNewHighCht = "https://www.finviz.com/screener.ashx?v=351&f=ind_exchangetradedfund,sh_avgvol_o100,ta_change_u2,ta_highlow52w_nh&ft=4&o=-change"
stkNewHighCht ="https://www.finviz.com/screener.ashx?v=351&f=ind_stocksonly,sh_avgvol_o100,ta_change_u2,ta_highlow52w_nh&ft=4&o=-change"
fatmanCht = "https://www.finviz.com/screener.ashx?v=351&t=AMZN,TSLA,MSFT,GOOGL,NFLX,FB&ta=0&o=perf1w"
faganmsmCht = "https://www.finviz.com/screener.ashx?v=351&t=FB,AAPL,GOOGL,AMZN,NFLX,MSFT,SBUX,NKE&ta=0"
etfLongBrkCht = "https://www.finviz.com/screener.ashx?v=351&f=ind_exchangetradedfund,sh_avgvol_o400,sh_price_o5,ta_averagetruerange_o1.5,ta_change_u2,ta_highlow20d_b0to3h,ta_highlow50d_b0to3h,ta_sma20_pa,ta_sma200_pa,ta_sma50_pa&ft=4&ta=0&o=-change"
stkLongBrkCht = "https://www.finviz.com/screener.ashx?v=351&f=ind_stocksonly,sh_avgvol_o400,sh_price_o5,ta_averagetruerange_o1.5,ta_change_u2,ta_highlow20d_b0to3h,ta_highlow50d_b0to3h,ta_sma20_pa,ta_sma200_pa,ta_sma50_pa&ft=4&ta=0&o=-change"

# Functions
def ScreenerArgumnets(eventPressed): 
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
        'Sector ETF': etfSecCht,
        'Simple Breakout Scan ETF': etfBrkCht,
        'Simple Breakout Scan STK': stkBrkCht,
        'New High ETF': etfNewHighCht,
        'New High STK': stkNewHighCht,
        'FATMAN': fatmanCht,
        'FAGANMSN': faganmsmCht,
        'Long Breakout Setup ETF': etfLongBrkCht,
        'Long Breakout Setup STK': stkLongBrkCht, 
    }
    # get() method of dictionary data type returns  
    # value of passed argument if it is present  
    # in dictionary otherwise second argument will 
    # be assigned as default value of passed argument 
    return switcher.get(eventPressed, "nothing")
        
# Main Program

sg.theme('BluePurple')

layout = [[sg.Text('ETF Performance:'), sg.Text(size=(40,1), key='-OUTPUT-')],
          [sg.Input(key='-IN-')],
          [sg.Button('Open etfscreen age'), sg.Button('File'), sg.Button('Execute')], 
          [sg.Text('Sectors Performance')], 
          [sg.Button('Sectors Daily'), 
           sg.Button('Sectors 1W'), 
           sg.Button('Sectors 4W'),  
           sg.Button('Sectors 13W'), 
           sg.Button('Sectors 26W'), 
           sg.Button('Sectors 52W'),  
           sg.Button('Sectors YTD')],
          [sg.Text('Charts')],
          [sg.Button('Sector ETF'),
           sg.Button('Simple Breakout Scan ETF'),
           sg.Button('Simple Breakout Scan STK'),
           sg.Button('New High ETF'),
           sg.Button('New High STK'),
           sg.Button('Long Breakout Setup ETF'),
           sg.Button('Long Breakout Setup STK'),
           sg.Button('FATMAN'),
           sg.Button('FAGANMSN')],
          [sg.Text('Close')],
          [sg.Button('Exit')]]

window = sg.Window('Pattern 2B', layout)

while True:  # Event Loop
    event, values = window.read()
    print(event, values)
    
    if event in (None, 'Exit'):
        break
    
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

    # Performance printing on Windows
    if (event in buttonSecList):
        paramList = ScreenerArgumnets(event)
        print(paramList)
        if len(paramList) > 1:
            screenResult = TktScreeenTable(sectorsTktList, paramList[0], paramList[1])
            sg.Print(size=sectorsPerfWindow, do_not_reroute_stdout=False)
            print(screenResult)
            sg.Print( do_not_reroute_stdout=True)
      
window.close()
'''
Created on Apr 11, 2020

@author: toroboltan

The purpose of this app is from a list of TKTs introduced in a list:

   1) Check which list TKT belongs to 
   2) Create an entry in an excel file to calculate faster risk/reward
'''
import PySimpleGUI as sg

from etfutils import TktScreeenTable


import os
import sys
'''
This window will change the value assigned to new_date and old_date_header in date_setter.py script to the value 
what the user introduces

new_date = r"'20200409'"
old_date_header = "filePrefix = '2020"

and then it will run date_setter.py
'''

# Parameters to be used for GUI presentation

sectorsOverWindow = (157,28)
sectorsPerfWindow = (190,28)
tktApp = 'tkt_eval_gui'
inputMsg = 'Introduce TKTs separated by commas:'
txtSize = (40,1)
inputKey = '-IN-'
outputKey = '-OUTPUT-'
execKey = 'Execute'
exitKey = 'Exit'

script_path = r'C:\EclipseWorkspaces\csse120\kirk_tools'
script_list = ['date_setter.py']
tktPath = r'D:\jeronimo\trading\etf'


lineStartToChange1 = 'new_date =' 
lineStartToChange2 = 'old_date_header ='

# Sectors List
sectorsTktList = ['IWM','XLF','EEM','XLE','XLK',
                  'XLV','IYT','XLU','XLI','XLY',
                  'IYR','XLP','XLB','TLT','GLD',
                  'UUP','RTH','IYZ','SMH','DBC','USO']

# Parameters to be used for Performance Table
performanceTable = "Performance"
perf1w = "-perf1w"
perf4w = "-perf4w"
perf13w = "-perf13w"
perf26w = "-perf26w"
perf52w = "-perf52w"
perfytd = "-perfytd"

# Parameters to be used for Overview Table
overviewTable = "Overview"
change = "-change"

# To implement a case

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

# Nain Program

sg.theme('BluePurple')

layout = [[sg.Text(inputMsg), sg.Text(size=txtSize, key=outputKey)],
          [sg.Input(key=inputKey)],
          [sg.Button(execKey), sg.Button(exitKey)]]

window = sg.Window(tktApp, layout)

while True:  # Event Loop
    event, values = window.read()
    print(event, values)
    
    if event in  (None, exitKey):
        break
    
    if event == 'File':
        fname = sys.argv[1] if len(sys.argv) > 1 else sg.popup_get_file('Document to open', initial_folder=tktPath)
        
        if not fname:
            sg.popup("Cancel", "No filename supplied")
            raise SystemExit("Cancelling: no filename supplied")
        else:
            window['-OUTPUT-'].update(fname)
            window['-IN-'].update(fname)
            
    if event == execKey:
        tktList = values['-IN-']
        print(tktList)
        
    if (event != 'File') and (event != 'Execute'):
        paramList = ScreenerArgumnets(event)
        print(paramList)
        if len(paramList) > 1:
            screenResult = TktScreeenTable(sectorsTktList, paramList[0], paramList[1])
            sg.Print(size=sectorsPerfWindow, do_not_reroute_stdout=False)
            print(screenResult)
            sg.Print( do_not_reroute_stdout=True)
      
window.close()
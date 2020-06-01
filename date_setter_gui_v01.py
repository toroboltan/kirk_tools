'''
Created on Apr 11, 2020

@author: CEVDEA
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


script_path = r'C:\EclipseWorkspaces\csse120\kirk_tools'
script_list = ['date_setter.py']
tktPath = r'D:\jeronimo\trading\etf'
sectorsOverWindow = (157,28)
sectorsPerfWindow = (190,28)

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

layout = [[sg.Text('Your typed chars appear here:'), sg.Text(size=(40,1), key='-OUTPUT-')],
          [sg.Input(key='-IN-')],
          [sg.Button('File'),sg.Button('Execute'), 
           sg.Button('Sectors Daily'), sg.Button('Sectors 1W'), sg.Button('Sectors 4W'),  sg.Button('Sectors 13W'), sg.Button('Sectors 26W'), sg.Button('Sectors 52W'),  sg.Button('Sectors YTD'), sg.Button('Exit')]]

window = sg.Window('Pattern 2B', layout)

while True:  # Event Loop
    event, values = window.read()
    print(event, values)
    
    if event in  (None, 'Exit'):
        break
    
    if event == 'File':
        fname = sys.argv[1] if len(sys.argv) > 1 else sg.popup_get_file('Document to open', initial_folder=tktPath)
        
        if not fname:
            sg.popup("Cancel", "No filename supplied")
            raise SystemExit("Cancelling: no filename supplied")
        else:
            window['-OUTPUT-'].update(fname)
            window['-IN-'].update(fname)
            
    if event == 'Execute':
        fileinfo = values['-IN-']
        print(type(fileinfo))
        fileinfoList = fileinfo.split("/")
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

    if (event != 'File') and (event != 'Execute'):
        paramList = ScreenerArgumnets(event)
        print(paramList)
        if len(paramList) > 1:
            screenResult = TktScreeenTable(sectorsTktList, paramList[0], paramList[1])
            sg.Print(size=sectorsPerfWindow, do_not_reroute_stdout=False)
            print(screenResult)
            sg.Print( do_not_reroute_stdout=True)
      
window.close()
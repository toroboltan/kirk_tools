'''
Created on Apr 11, 2020

@author: toroboltan

The purpose of this app is from a list of TKTs introduced in a list:

   1) Check which list TKT belongs to 
   2) Create an entry in an excel file to calculate faster risk/reward
'''
import PySimpleGUI as sg
import pandas as pd
import os
import sys

from etfutils import TktScreeenTable

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

# Parameters to be used to pull Bucktes Information
listPath = r'C:\Users\jeron\Google Drive\trading\kirk\2019\Listas'
listFile = '2018_ListasTrack.xlsx'
tktPath = r'D:\jeronimo\trading\etf'
listSheet = 'ListasTrack'
balanceSheet = 'BalancesShort'


# To implement a case
# This class will have two main fields
#  1) screen
#  2) tktlist

class screenTktItem():

    nameScreen_s = ''
    tktScreenList = []
    sep_s = '->'
    
    def __init__(self, line):
        intermList = line.split(self.sep_s)
        self.nameScreen_s = intermList[0]
        self.tktScreenList = intermList[1].split(',')

# Main Program

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
        # Read the values and stored them as a list
        tktList = values['-IN-']
        tktLines = tktList.splitlines()
        # if there are elements in the list
        if(len(tktLines) > 0):
            sourceTktList = []
            for col in tktLines:
                sourceTktList.append(screenTktItem(col))
            for item in sourceTktList:
                print(item.nameScreen_s)
                print(item.tktScreenList)
                
            # goto path where list files are
            os.chdir(listPath)
            pdTktList = pd.read_excel(listFile, sheet_name= listSheet)
            pdBalList = pd.read_excel(listFile, sheet_name= balanceSheet)
            # printing cash available per bucket
            for col in pdBalList.columns:
                print(pdBalList.loc[0].at[col])
                print(type(pdBalList.loc[0].at[col]))
            for col in pdTktList.columns:
                print(pdTktList[col].dropna().to_list())
                
window.close()
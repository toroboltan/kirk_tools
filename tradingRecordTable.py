# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 23:04:22 2020

@author: jeron
"""

import PySimpleGUI as sg
import os
import pandas as pd


## Functions

def openTradingTable(tablePath, tableFile, tableSheet):
    # Reading the file
    os.chdir(tablePath)
    df = pd.read_excel(tableFile, sheet_name=tableSheet)
    return df


## File information
tablePath = r'C:\Users\jeron\Google Drive\trading\kirk\2019\active trading'
tableFile = "2020_MoneyManagementSpreadsheet.xlsx"
tableSheet = "TKT_TT_PY_2019_MST"

## PySimpleGUI Parameters
sectorsOverWindow = (157,28)
sectorsPerfWindow = (190,28)
buttonTradingTable = 'Open Trading Table'


layout = [[sg.Text('ETF Performance:'), sg.Text(size=(40,1), key='-OUTPUT-')],
          [sg.Button(buttonTradingTable)], 
          [sg.Button('Exit')]]



# Main Program

window = sg.Window('tradingTableReader', layout)

while True:  # Event Loop
    event, values = window.read()
    print(event, values)
    
    if event in (None, 'Exit'):
        break
    
    if event == buttonTradingTable:
        dfTrading = openTradingTable(tablePath, tableFile, tableSheet)
            
window.close()
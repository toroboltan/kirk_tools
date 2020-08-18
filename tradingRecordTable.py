# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 23:04:22 2020

@author: jeron
"""

import PySimpleGUI as sg
import os
import sys

## File information
tablePath = r'C:\Users\jeron\Google Drive\trading\kirk\2019\active trading'
tableFile = "2020_MoneyManagementSpreadsheet.xlsx"
tableSheet = "TKT_TT_PY_2019_MST"

## PySimpleGUI Parameters
sectorsOverWindow = (157,28)
sectorsPerfWindow = (190,28)


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
          [sg.Button('US Markets'),
           sg.Button('Sector ETF'),
           sg.Button('ETF Perf Daily'),
           sg.Button('ETF Perf Weekly'),         
           sg.Button('Simple Breakout Scan ETF'),
           sg.Button('Simple Breakout Scan STK'),
           sg.Button('New High ETF'),
           sg.Button('New High STK'),
           sg.Button('Long Breakout Setup ETF'),
           sg.Button('Long Breakout Setup STK'),
           sg.Button('FATGANMSN')],
          [sg.Text('*** Candidates ***')],
          [sg.Text('From US Markets :'), sg.InputText(key='etfUsMarkets')],
          [sg.Text('From Sectors :'), sg.InputText(key='etfSecCht')],
          [sg.Text('From ETF Performance Daily :'), sg.InputText(key='etfPerfDaily')],
          [sg.Text('From ETF Performance Weekly :'), sg.InputText(key='etfPerfWeekly')],
          [sg.Text('From Simple Breakout ETF :'), sg.InputText(key='etfBrkCht')],
          [sg.Text('From Simple Breakout STK :'), sg.InputText(key='stkBrkCht')],
          [sg.Text('From New High ETF :'), sg.InputText(key='etfNewHighCht')],
          [sg.Text('From New High STK :'), sg.InputText(key='stkNewHighCht')],
          [sg.Text('From Long Breakout Setup ETF :'), sg.InputText(key='etfLongBrkCht')],
          [sg.Text('From Long Breakout setup STK :'), sg.InputText(key='stkLongBrkCht')],
          [sg.Text('From FATGANMSN :'), sg.InputText(key='fatganmsn')],
          [sg.Text('******************')],
          [sg.Button(buttonProcess)],
          [sg.Button('Exit')]]



# Main Program

window = sg.Window('TorolGui', layout)

while True:  # Event Loop
    event, values = window.read()
    print(event, values)
    
    if event in (None, 'Exit'):
        break
    
    if event == 'Open etfscreen age':
        openweb("chrome", [etfPerLnk])
            
window.close()
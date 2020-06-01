'''
Created on Apr 19, 2020

I will use this script to help me speed my price calculation and information collection.

It will collect a list of TKTs from clipboard with the following format

"bucket" -> tkt1, tkt2, tkt3,...

Sectors -> RTH, SMH, XLV, XLY, TTL, GLD, UUP, RTH
ETF -> XBI, BBH, AMLP, PTH, ARKG, ARKW, ARKK
New High -> NFLX, ELMD, ALNY, WING, VTRX, SGEN, LLY, FIVN, OKTA, CDNS, WMT, MKTX
Winners -> LOVE, TROX, SHOP, BA, WMS, SGRY, JACK, BLUE
News - > BA, WMT, PG, XOM, UPS, BRK-B, VZ, VMW

At the end the list I'm expecting is something similar

Lista 
tkt1, price
tkt2, price

If there is a ticket repeated between different buckets it will consilidate it in the appropiated list



Steps:

    Read from clipboard TKT info to be used
@author: CEVDEA
'''

import PySimpleGUI as sg
import finviz
from etfutils import TktOverview

newLineChars = '\r\n'
newLineChar = '\n'
lineSeparator = ' -> '
commaSeparator = ', '
tktPath = r'C:\temp\etf\pricestocheck'
listasPath = r'C:\Users\cevdea\Google Drive\trading\kirk\2019\Listas'
listasFile = '2018_ListasTrack.xlsx'
tktFile = '20200419.txt'
sector = 'Sector'
industry = 'Industry'
price = 'Price'
tktListEval = []
res = {} 

sg.theme('Dark Blue 3')  # please make your windows colorful

layout = [[sg.Text('Filename')],
            [sg.Input(key='-IN-'), sg.FileBrowse(initial_folder=tktPath)],
            [sg.OK(), sg.Cancel()] ]

window = sg.Window('Get filename example', layout)

while True:  # Event Loop
    event, values = window.read()
    print(event, values)
    if event in  (None, 'Cancel'):
        break
    if event == 'OK':
        print(values)
        tktFile = values['-IN-']
        f = open(tktFile,"r")
        text = f.readlines()
        for linea in text:
            linea = linea.rstrip(newLineChar)
            lineaList = linea.split(lineSeparator)
            res[lineaList[0]] = lineaList[1]
        for key in res.keys():
            print("***** " + key + " *****")
            tktList = res[key].split(commaSeparator)
            for tkt in tktList:
                print(tkt)
                if tkt not in tktListEval:
                    tktListEval.append(tkt)
                    screenObj = TktOverview(tkt).get(0)
                    print(tkt + " " + screenObj[sector] + " " + screenObj[industry] + " " + screenObj[price])
        break
        
window.close()




#text = pyperclip.paste()
#textList = text.split(newLineChars)
#print(textList)













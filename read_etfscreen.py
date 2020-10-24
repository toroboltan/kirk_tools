import requests
import pandas as pd
import updatemms as upm
import kirkconstants as kc

def FormatFinvizDf(df):
    # Drop columns with numbers
    df = df.drop(0 ,axis = 1)
    # Dataframe headers
    oldHeaders = df.columns.to_list()
    newHeaders = df.loc[0,:].to_list()
    # using dictionary comprehension 
    # to convert lists to dictionary 
    res = {oldHeaders[j]: newHeaders[j] for j in range(len(newHeaders))}
    df.rename(columns = res, inplace = True)
    df = df.drop(0)
    return df

def ReadFirstFinvizScreener(url, header):
    ''' This function returns number of tickets and asociated dataframe '''
    tablas = ReadFinvizTablas(url, header)
    tabla = tablas[15]
    tktTotal = int(tabla[0][0].split(' ')[1])
    tabla = tablas[16]
    dft = FormatFinvizDf(tabla)
    return(tktTotal,dft)

def ReadFinvizTablas(url, header):
    r = requests.get(url, headers=header)
    tablas = pd.read_html(r.text)
    return tablas

url_etf = f'https://finviz.com/screener.ashx?v=111&f=ind_exchangetradedfund&ft=4'
url_stk = f'https://finviz.com/screener.ashx?v=111&f=ind_stocksonly&ft=4'

header = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"
}

testPath = kc.testPath
testFileOut = kc.testFileOut

i = 0
tktTotal = 0
tkt_per_page = 20
dft = pd.DataFrame()

url_base = url_stk

tktTotal, dft = ReadFirstFinvizScreener(url_base, header)

'''
for tabla in tablas:
    #print('tabla ' + str(i))
    #print(tabla)
    if i == 15:
        print(type(tabla))
        print(tabla[0][0])
        tktTotal = int(tabla[0][0].split(' ')[1])
        print(str(tktTotal))
        #break
    if i == 16:
        dft = FormatFinvizDf(tabla)
    i += 1
'''

for counter in range(tkt_per_page + 1 ,tktTotal, tkt_per_page):
    dft2 = pd.DataFrame()
    url_suffix = f'&r='+str(counter)
    url_counter = url_base + url_suffix
    print(url_counter)
    #r = requests.get(url_counter, headers=header)
    #tablas = pd.read_html(r.text)
    tablas = ReadFinvizTablas(url_counter, header)
    tabla = tablas[16]
    dft2 = FormatFinvizDf(tabla)
    dft = pd.concat([dft, dft2], ignore_index=True)

upm.ExportDfToCsv(dft, testPath, testFileOut)



'''
Created on Sep 9, 2019
This program will read the txt file generated from copy/paste the webpage

https://www.etfscreen.com/performance.php?wl=0&s=Rtn-1d%7Cdesc&t=6&d=i&ftS=no&ftL=no&vFf=dolVol21&vFl=gt&vFv=1000000&udc=default&d=i

Selecting apart from the default Short Funds = No and Leverage Funds = NO

The objective is to get a list of top/worst 10 ETF daily

Tasks tpo do:

1) Open the file
2) Read only the lines of interest
    lines of interest are
        From: two line after "Name"
        To: line before  "symbols listed"
3) Create a class that represents each TKT
4) Store each ticket in a csv file/pandas/database - but before that I will try to dump it in a file

@author: cevdea
'''
import datetime
import pandas as pd
from etfclass import tktEtfScreen
from etfutils import tktFileReader, tktParserFromTktListToDataframeList, tktDfPrintTopBottom, etfDailyDataList

cons_flag_normal = 0
cons_flag_proto = 1

'''
    Main program
'''
filePath_s = r'D:\jeronimo\trading\etf'
filePrefix = '20201026'
fileName_s = filePrefix + '_etfp.txt'

controlFlag = True
formatSource = 'txt'
flag_exec = 1
columns_dataframe = ['Name', 'Symbol', 'RSf', 'Price', 'Rtn-1d' , 'Rtn-5d', 'Rtn-1mo', 'Rtn-3mo', 'Rtn-6mo', 'Rtn-1yr', 'vol-21']
htmlLine1 = '<tr><td><input type="checkbox" name="cSyms[]" value="MLPA" ></td><td  class="taL"><img src="/images/chartBtn.gif" class="popChtLink" style="float: right;" data-sym="MLPA" alt="popup"><a href="/price-chart.php?s=MLPA">Global X MLP ETF</a></td><td>MLPA</td><td bgcolor="#c5eac5">21.27</td><td bgcolor="#c9ecc9">2.41</td><td bgcolor="#def8de">3.79</td><td bgcolor="#dff8df">4.81</td><td bgcolor="#ffebeb">-0.12</td><td bgcolor="#e7fde7">1.89</td><td bgcolor="#ffdcdc">-6.67</td><td bgcolor="#ebffeb">6m</td></tr>'
htmlLine2 = '<tr><td><input type="checkbox" name="cSyms[]" value="VSGX" ></td><td  class="taL"><img src="/images/chartBtn.gif" class="popChtLink" style="float: right;" data-sym="VSGX" alt="popup"><a href="/price-chart.php?s=VSGX">Vanguard ESG International Stock ETF</a></td><td>VSGX</td><td bgcolor="#9ad29a">44.79</td><td bgcolor="#e3fae3">0.59</td><td bgcolor="#e4fbe4">2.03</td><td bgcolor="#d8f5d8">7.48</td><td bgcolor="#e4fbe4">3.01</td><td bgcolor="#e6fce6">2.28</td><td>n/a</td><td bgcolor="#ebffeb">2m</td></tr>'

topNumber = 10
const1D = '1D'
const1W = '1W'
const1M = '1M'
const1Q = '1Q'
const1H = '1H'
const1Y = '1Y'

tktLines_L = []
tktList_L=[]
outputDir = filePath_s


current_dt = datetime.datetime.now()
print ("**** Begin ****" + str(current_dt))

if flag_exec == cons_flag_normal :

    
    tktLines_L = tktFileReader(filePath_s, fileName_s, formatSource)
    print('number of tickets read : ' + str(len(tktLines_L)))
    etf_list_dict = etfDailyDataList()
    for line in tktLines_L:
        tktList_L.append(tktEtfScreen(line, formatSource, flag_exec, etf_list_dict))
    print('number of tickets tkt objects : ' + str(len(tktList_L)))
    
    if len(tktList_L) > 0:
    
        # Tinkering with pandas
        if controlFlag :
            print('*** Tinkering with Pandas ***')
            values_dataframe = []
            values_dataframe = tktParserFromTktListToDataframeList(tktList_L)
            tkt_dataframe = pd.DataFrame(values_dataframe, columns = columns_dataframe)
    
            print('************************')
            tktDfPrintTopBottom(tkt_dataframe, topNumber, const1D, filePrefix, outputDir)
            print('------------------------')
            tktDfPrintTopBottom(tkt_dataframe, topNumber, const1W, filePrefix, outputDir)
            print('------------------------')
            tktDfPrintTopBottom(tkt_dataframe, topNumber, const1M, filePrefix, outputDir)
            print('------------------------')
            tktDfPrintTopBottom(tkt_dataframe, topNumber, const1Q, filePrefix, outputDir)
            print('------------------------')
            tktDfPrintTopBottom(tkt_dataframe, topNumber, const1H, filePrefix, outputDir)
            print('------------------------')
            tktDfPrintTopBottom(tkt_dataframe, topNumber, const1Y, filePrefix, outputDir)
            print('************************')
    
    current_dt = datetime.datetime.now()
    print ("**** End ****" + str(current_dt))
    
elif flag_exec == cons_flag_proto:
    print("This is the proto part")

    tktLines_L = tktFileReader(filePath_s, fileName_s, formatSource)
    print('number of tickets read : ' + str(len(tktLines_L)))
    etf_list_dict = etfDailyDataList()
    for line in tktLines_L:
        tktList_L.append(tktEtfScreen(line, formatSource, flag_exec, etf_list_dict))
    print('number of tickets tkt objects : ' + str(len(tktList_L)))
    
    if len(tktList_L) > 0:
    
        # Tinkering with pandas
        if controlFlag :
            print('*** Tinkering with Pandas ***')
            values_dataframe = []
            values_dataframe = tktParserFromTktListToDataframeList(tktList_L)
            tkt_dataframe = pd.DataFrame(values_dataframe, columns = columns_dataframe)
    
            print('************************')
            tktDfPrintTopBottom(tkt_dataframe, topNumber, const1D, filePrefix, outputDir)
            print('------------------------')
            tktDfPrintTopBottom(tkt_dataframe, topNumber, const1W, filePrefix, outputDir)
            print('------------------------')
            tktDfPrintTopBottom(tkt_dataframe, topNumber, const1M, filePrefix, outputDir)
            print('------------------------')
            tktDfPrintTopBottom(tkt_dataframe, topNumber, const1Q, filePrefix, outputDir)
            print('------------------------')
            tktDfPrintTopBottom(tkt_dataframe, topNumber, const1H, filePrefix, outputDir)
            print('------------------------')
            tktDfPrintTopBottom(tkt_dataframe, topNumber, const1Y, filePrefix, outputDir)
            print('************************')
    
    current_dt = datetime.datetime.now()
    print ("**** End ****" + str(current_dt))

    
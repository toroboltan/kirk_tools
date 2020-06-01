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
from etfutils import stkDailyDataO
'''
    Main program
'''
filePath_s = r'D:\jeronimo\trading\etf'
filePrefix = '20200529'
fileName_s = filePrefix + '_etfp.txt'
controlFlag = True
formatSource = 'txt'
columns_dataframe = ['Name', 'Symbol', 'RSf', 'Price', 'Rtn-1d' , 'Rtn-5d', 'Rtn-1mo', 'Rtn-3mo', 'Rtn-6mo', 'Rtn-1yr', 'vol-21']
htmlLine1 = '<tr><td><input type="checkbox" name="cSyms[]" value="MLPA" ></td><td  class="taL"><img src="/images/chartBtn.gif" class="popChtLink" style="float: right;" data-sym="MLPA" alt="popup"><a href="/price-chart.php?s=MLPA">Global X MLP ETF</a></td><td>MLPA</td><td bgcolor="#c5eac5">21.27</td><td bgcolor="#c9ecc9">2.41</td><td bgcolor="#def8de">3.79</td><td bgcolor="#dff8df">4.81</td><td bgcolor="#ffebeb">-0.12</td><td bgcolor="#e7fde7">1.89</td><td bgcolor="#ffdcdc">-6.67</td><td bgcolor="#ebffeb">6m</td></tr>'
htmlLine2 = '<tr><td><input type="checkbox" name="cSyms[]" value="VSGX" ></td><td  class="taL"><img src="/images/chartBtn.gif" class="popChtLink" style="float: right;" data-sym="VSGX" alt="popup"><a href="/price-chart.php?s=VSGX">Vanguard ESG International Stock ETF</a></td><td>VSGX</td><td bgcolor="#9ad29a">44.79</td><td bgcolor="#e3fae3">0.59</td><td bgcolor="#e4fbe4">2.03</td><td bgcolor="#d8f5d8">7.48</td><td bgcolor="#e4fbe4">3.01</td><td bgcolor="#e6fce6">2.28</td><td>n/a</td><td bgcolor="#ebffeb">2m</td></tr>'

tktLines_L = []
tktList_L=[]
outputDir = filePath_s


current_dt = datetime.datetime.now()
print ("**** Begin ****" + str(current_dt))

stkDailyDataO(filePrefix, outputDir)

current_dt = datetime.datetime.now()
print ("**** End ****" + str(current_dt))
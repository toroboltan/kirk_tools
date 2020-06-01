'''
Created on Jan 28, 2019

@author: CEVDEA
'''
from requests import get
import os
import datetime

#Variables
filePath_s = r'C:\temp\etf'
fileName_s = r'test_etfp.txt'
headers = ({'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
sapo = "https://www.etfscreen.com/performance.php"

#Begin
current_dt = datetime.datetime.now()
print ("**** Begin ****" + str(current_dt))

#Read web page
response = get(sapo, headers=headers)

#Write webpage output to text file
os.chdir(filePath_s)
fileOutHandler_file = open(fileName_s, 'w')
print('file opened')
fileOutHandler_file.write(response.text[:])
print('file written')
fileOutHandler_file.close()
print('file closed')

#End
current_dt = datetime.datetime.now()
print ("**** End ****" + str(current_dt))

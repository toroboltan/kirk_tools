'''
Created on Jan 7, 2020

@author: CEVDEA
'''

import datetime
import os

'''
    Main program
'''
script_path = r'C:\EclipseWorkspaces\csse120\kirk_tools'
script_list = ['etf_spy_dia_parser.py',
               'stk_overview_parser.py',
               'stk_performance_parser.py',
               'stk_technical_parser.py',
                'etfscreen_parser.py']

new_date = r"'20200529'"
old_date_header = "filePrefix = '2020"
fileName_s = str(new_date) + '_etfp.txt'
filePath_s = r'D:\jeronimo\trading\etf'



current_dt = datetime.datetime.now()
print ("**** Begin date_setter ****" + str(current_dt))

os.chdir(script_path)

for script_file in script_list:
    print('BEGIN Filename is ' + script_file)
    f = open(script_file,"r")
    lines = f.readlines()
    f.close()
    for i, line in enumerate(lines):
        if(line.startswith(old_date_header)):
            line_list = line.split("=")
            line_list[1] = new_date
            lines[i] =  "= ".join(line_list) + '\n'
    f = open(script_file, "w")
    f.write("".join(lines))
    f.close()
    print('END Filename is ' + script_file)  



for script_file in script_list:
    os.system('python ' + script_file)

current_dt = datetime.datetime.now()
print ("**** End date_setter ****" + str(current_dt))
'''
Created on Sep 5, 2020

@author: jeron
'''

## Parameters & Constants update_mms

# File information
tablePath = r'C:\Users\jeron\Google Drive\trading\kirk\2020\active trading'
tableFile = "2020_MoneyManagementSpreadsheet.xlsx"
tableSheet = "trade_log"
tableFileOut = "2020_MoneyManagementSpreadsheet_testb.xlsx"


## Parameters & Constants date_setter_gui_v01

# Environment variables
listPath = r'C:\Users\jeron\Google Drive\trading\kirk\2020\Listas'
fileList = "2018_ListasTrack.xlsx"
sheetList = "Symbols"
script_path = r'C:\EclipseWorkspaces\csse120\kirk_tools'
script_list = ['date_setter.py']
tktPath = r'D:\jeronimo\trading\etf'


## Parameters & Constants tradingutils

# trade parameters
risk = 1
commision = 2
stoploss_perc = 8
rwd_rsk_factor = 3

# File information
candPath = r'C:\Users\jeron\Google Drive\trading\kirk\2020\active trading'
candFile = "2020_KirkCandidatesManagementSpreadsheet.xlsx"
candSheet = "tkt_tt_py_2019_msft"

bucketPath = r'C:\Users\jeron\Google Drive\trading\kirk\2020\Listas'
bucketFile = "2018_ListasTrack.xlsx"
bucketSheet = "Symbols"
balanceSheet = "BalancesShort"

actTradesPath = r'C:\Users\jeron\Google Drive\trading\kirk\2020\active trading'
actTradesFile = "2020_MoneyManagementSpreadsheet_testb.xlsx"
actTradestSheet = "trade_log"

posTradesPath = r'C:\Users\jeron\Google Drive\trading\kirk\2020\possibleTrades'
posTradeRawFileSfx = "PossibleTradesRaw.csv"
posTradeFinalFileSfx = 'PossibleTradesFinal.csv'

# Years to be selected
year_prefix = 2020

# Excel info
code_col = 1
date_col = 10
price_col = 11
start_row = 15
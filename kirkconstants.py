'''
Created on Sep 5, 2020

@author: jeron
'''

## Parameters & Constants mgtpb
# File information
pbPath = r'C:\Users\jeron\Google Drive\trading\kirk\2021\active trading'
pbFile = "2021_KirkCandidatesManagementSpreadsheetTest.xlsx"
pbSheet = "tkt_tt_py"

## Parameters & Constants update_mms
# File information
tablePath = r'C:\Users\jeron\Google Drive\trading\kirk\2021\active trading'
tableFile = "2021_MoneyManagementSpreadsheet.xlsx"
tableSheet = "trade_log"
tableFileOut = "2021_MoneyManagementSpreadsheet.xlsx"

## Parameters & Constants date_setter_gui_v01
# Environment variables
listPath = r'C:\Users\jeron\Google Drive\trading\kirk\2021\Listas'
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
candPath = r'C:\Users\jeron\Google Drive\trading\kirk\2021\active trading'
candFile = "2021_KirkCandidatesManagementSpreadsheet.xlsx"
candSheet = "tkt_tt_py"

bucketPath = r'C:\Users\jeron\Google Drive\trading\kirk\2021\Listas'
bucketFile = "2018_ListasTrack.xlsx"
bucketSheet = "Symbols"
balanceSheet = "BalancesShort"

actTradesPath = r'C:\Users\jeron\Google Drive\trading\kirk\2021\active trading'
actTradesFile = "2021_MoneyManagementSpreadsheet.xlsx"
actTradestSheet = "trade_log"

posTradesPath = r'C:\Users\jeron\Google Drive\trading\kirk\2021\possibleTrades'
posTradeRawFileSfx = "PossibleTradesRaw"
posTradeFinalFileSfx = 'PossibleTradesFinal'

etfChkPath = r'C:\Users\jeron\Google Drive\trading\kirk\2021\possibleTrades'
etfChkFileSfx = "EtfCheckRaw.csv"

# Years to be selected
# 1899 is the year that is set when a date type cell in excel is set to -1
year_prefix = 1899

# Excel info
code_col = 1
date_col = 10
price_col = 11
start_row = 15

## Parameters for scrapetfscreen
# File information
testPath = r'C:\tmp\test'
testFileIn = "testIn.csv"
testSheet = "testSheet"
testFileOut = "testOut.csv"

# Pickle information
fileNamePickle = 'etf_screen_df.pickle'

# SQL information
db_prefix = 'mysql+pymysql://root:@localhost:3360/'
db_struc_etf = 'tradingdb'
db_table_etf = 'etfscreen'
db_table_cand = 'tkt_candidates'

topNumber = 10
const1D = '1D'
const1W = '1W'
const1M = '1M'
const1Q = '1Q'
const1H = '1H'
const1Y = '1Y'

## Parameters & Constants dailycandidates
# File information
dcPath = r'C:\Users\jeron\Google Drive\trading\kirk\2021\active trading'
dcFile = "2021_ActivityTrackerSpreadsheet.xlsx"
dcSheet = "daily_cand"
dbCandTable = "daily_tkts"

# API keys - alphavantage
alphavantage_key = '3SAVQIE3TDG93UDE'

# API keys - alpaca
ALPACA_API_KEY = 'PKZRT7YHIDBSQS36RCNX'
ALPACA_SECRET_KEY = '4flYAGGWHI4eJ81OlBywLK3GTc1Lxu6I6gZgAOHu'
ALPACA_PAPER_END_POINT = 'https://paper-api.alpaca.markets'
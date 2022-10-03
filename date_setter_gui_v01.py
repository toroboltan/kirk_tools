import PySimpleGUI as sg
import os
import sys
import webbrowser
from etfutils import TktScreeenTable
import pandas as pd
import updatemms as up
import tradingutils as tu
import kirkconstants as kc
import scrapetfscreen as scetf
import dbhandler as dbh
import datetime
import dailycandidates as dcan

# Functions
def ScreenerArguments(eventPressed): 
    switcher = { 
        'Sectors Daily': [overviewTable, change], 
        'Sectors 1W': [performanceTable, perf1w],
        'Sectors 4W': [performanceTable, perf4w],
        'Sectors 13W': [performanceTable, perf13w],
        'Sectors 26W': [performanceTable, perf26w], 
        'Sectors 52W': [performanceTable, perf52w],
        'Sectors YTD': [performanceTable, perfytd] 
    } 
    # get() method of dictionary data type returns  
    # value of passed argument if it is present  
    # in dictionary otherwise second argument will 
    # be assigned as default value of passed argument 
    return switcher.get(eventPressed, "nothing")

def openweb(browser="", sites=[]):
    if browser == "chrome":
        chromedir= 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
    for site in sites:
        webbrowser.get(chromedir).open(site)

def chartsArgumnets(eventPressed): 
    switcher = {
        'US Markets': etfUsMarkets,
        'Sector ETF': etfSecCht,
        'ETF Perf Daily' : etfPerf1DUp,
        'ETF Perf Weekly' : etfPerf1WUp,       
        'Simple Breakout Scan ETF': etfBrkCht,
        'Simple Breakout Scan STK': stkBrkCht,
        'New High ETF': etfNewHighCht,
        'New High STK': stkNewHighCht,
        'FATGANMSN': fatganmsmCht,
        'Long Breakout Setup ETF': etfLongBrkCht,
        'Long Breakout Setup STK': stkLongBrkCht,
        'Major News': majorNewsCht,
        'Most Shorted Stocks': stkShortSquz,
        'Break Down Setups' : stkShortBrkCht,
        'indexes': kirkWlIndexes,
        'sectors': kirkWlSectors,
        'industries': kirkWlIndustries,
        'factors': kirkWlFactors,
        'fixed income': kirkWlFixIncome,
        'currencies': kirkWlCurrencies,
        'commodities': kirkWlCommodities,
        'global markets': kirkWlGlobalMarkets,
        'AwesomePort': kirkWlEvryAwsome,
        'leveraged': kirkWlLeveraged
    }
    # get() method of dictionary data type returns  
    # value of passed argument if it is present  
    # in dictionary otherwise second argument will 
    # be assigned as default value of passed argument 
    return switcher.get(eventPressed, "nothing")

def candList(textTkts):
    return textTkts.replace(" ", "").split(",")

def printBuckets(etfSet, stkSet, listPath, fileList, sheetList):
    # Reading the file
    os.chdir(listPath)
    df = pd.read_excel(fileList, sheet_name=sheetList)
    listBuckets = list(df.columns)
    # Finding buckets for etfs
    tktSetAssigned = set()
    tktSet = etfSet.union(stkSet)
    for bucket in listBuckets:
        print(bucket + ":")
        for tkt in tktSet:
            if (tkt in df[bucket].to_list()):
                print('\t' + tkt)
                tktSetAssigned.add(tkt)
    # Remove from combined set tkts already classified in bucktes
    for tkt in tktSetAssigned:
        tktSet.remove(tkt)
    # Printing Weekly Tkts
    print('Weekly:')
    for tkt in tktSet:
        print('\t' + tkt)

def initializeSets():
    # @TODO: This function has to initialize sets so candidates do not still have stored values for previos iteractions
    print('TODO - initializeSets')

def checkOpenPositions(tktToCheck_lst):
    # @TODO: This function checks if there are candidates with positions already open in the MoneyManagementTable If that is the case they are removed from the list values for previos iteractions 
    print('TODO - checkOpenPositions')   
    return tktToCheck_lst    

listPath = kc.listPath
fileList = kc.fileList
sheetList = kc.sheetList
script_path = kc.script_path
script_list = kc.script_list
tktPath = kc.tktPath

sectorsOverWindow = (157,28)
sectorsPerfWindow = (190,28)
lineStartToChange1 = 'new_date =' 
lineStartToChange2 = 'old_date_header ='
etfPref = "etf"
etfSet = set()
stkSet = set()
list_tktOpen = list()

# Parameters to be used for Performance Table
performanceTable = "Performance"
perf1w = "-perf1w"
perf4w = "-perf4w"
perf13w = "-perf13w"
perf26w = "-perf26w"
perf52w = "-perf52w"
perfytd = "-perfytd"

buttonSecList = ['Sectors Daily',
                 'Sectors 1W',
                 'Sectors 4W',
                 'Sectors 13W',
                 'Sectors 26W',
                 'Sectors 52W',
                 'Sectors YTD']

buttonChtList = ['indexes',
                 'sectors',
                 'industries',
                 'factors',
                 'fixed income',
                 'currencies',
                 'commodities',
                 'global markets',
                 'leveraged',
                 'AwesomePort',
                 'ETF Perf Daily',
                 'ETF Perf Weekly',
                 'New High ETF',
                 'New High STK',
                 'Simple Breakout Scan ETF',
                 'Simple Breakout Scan STK',
                 'Long Breakout Setup ETF',
                 'Long Breakout Setup STK',
                 'FATGANMSN',
                 'Major News',
                 'Most Shorted Stocks',
                 'Break Down Setups',]
                 
sectorsTktList = ['XLF','EEM','XLE','XLK',
                  'XLV','IYT','XLU','XLI',
                  'XLY','IYR','XLP','XLB',
                  'TLT','GLD','UUP','RTH',
                  'IYZ','SMH','DBC','USO']

textBoxList = ['kirkWlIndexes',
               'kirkWlSectors',
               'kirkWlIndustries',
               'kirkWlFactors',
               'kirkWlFixIncome',
               'kirkWlCurrencies',
               'kirkWlCommodities',
               'kirkWlGlobalMarkets',
               'kirkWlLeveraged',
               'kirkWlEvryAwsome',
               'etfPerfDaily',
               'etfPerfWeekly',
               'etfBrkCht',
               'stkBrkCht',
               'etfLongBrkCht', 
               'stkLongBrkCht', 
               'stkShortSquz',
               'stkShortBrkCht',
               'etfNewHighCht', 
               'stkNewHighCht', 
               'fatganmsn',
               'majorNewsCht']

buttonProcess = 'Process TKTs'
buttonShowCharts = 'Show Charts'
buttonOpenChartsScreen = 'Open Charts Screen'
buttonChkPlaysLong = 'Check Playbook Long'
buttonChkPlaysShort = 'Check Playbook Short'
buttonChkList = 'Check ETFs Lists'
buttonReadDb = 'read etfscreendb from db'
buttonReadPicFile = 'read etfscreendb from serial'
buttonWritePicDb = 'write serial to etfscreendb'
buttonExec = 'execute'
buttonConnectDb = 'Conectar DB'

buttonOpenLostTradesTracker = 'Open Lost Trades Tracker'
buttonOpenWonNotCompletedTracker = 'Open Won Not Completed'
buttonOpenWonCompletedTracker = 'Open Won Completed'
buttonOpenCandidatesTracker = 'Open Candidates'
buttonMoneyManagementSpsht = 'Money Mgmnt Spsht'
buttonOpenOrderManagementSpsht = 'Open Order Mgmnt'
buttonOpenBktListSpsht = 'Open Listas'
buttonOpenMonitorManagementSpsht = 'Open Monitor Mgmnt'
buttonOpenChangeTrackerSpsht = 'Open Change Tracker'

buttonBktCommodities = 'Commodities'
buttonBktCurrencies = 'Currencies'
buttonBktFANGAM = 'FANGAM'
buttonBktFixedIncome = 'Fixed Income'
buttonBktForeignMarktes = 'Foreign Markets'
buttonBktIndustries = 'Industries'
buttonBktMegatrends = 'Megatrends'
buttonBktLeveraged = 'Leveraged'
buttonBktSectors = 'Sectors'
buttonBktStyles = 'Styles'
buttonBktUsMarkets = 'US Markets'
buttonBktStocks = 'Stocks'


# Parameters to be used for Overview Table
overviewTable = "Overview"
change = "-change"

# Webpages Links
etfPerLnk = "https://www.etfscreen.com/performance.php?wl=0&s=Rtn-1d%7Cdesc&t=6&d=e&ftS=yes&ftL=no&vFf=dolVol21&vFl=gt&vFv=500000&udc=default&d=i"
etfUsMarkets = "https://www.finviz.com/screener.ashx?v=351&ft=4&t=SPY,IWC,IWM,DIA,OEF,MDY,QQQ&o=-change"
etfSecCht = "https://www.finviz.com/screener.ashx?v=351&ft=4&t=XLF,EEM,XLE,XLK,XLV,IYT,XLU,XLI,XLY,IYR,XLP,XLB,TLT,GLD,UUP,RTH,IYZ,SMH,DBC,USO&o=-change"
etfNewHighCht = "https://www.finviz.com/screener.ashx?v=351&f=ind_exchangetradedfund,sh_avgvol_o100,ta_change_u2,ta_highlow52w_nh&ft=4&o=-change"
stkNewHighCht ="https://www.finviz.com/screener.ashx?v=351&f=ind_stocksonly,sh_avgvol_o100,ta_change_u2,ta_highlow52w_nh&ft=4&o=-change"
fatganmsmCht = "https://finviz.com/screener.ashx?v=351&t=FB,AAPL,GOOGL,AMZN,NFLX,MSFT,TSLA,NVDA,TWTR,BABA,BIDU&o=-change"
majorNewsCht = "https://www.finviz.com/screener.ashx?v=320&s=n_majornews"

# Scans
etfLongBrkCht = "https://www.finviz.com/screener.ashx?v=351&f=ind_exchangetradedfund,sh_avgvol_o400,sh_price_o5,ta_averagetruerange_o1.5,ta_change_u2,ta_highlow20d_b0to3h,ta_highlow50d_b0to3h,ta_sma20_pa,ta_sma200_pa,ta_sma50_pa&ft=4&o=-change"
stkLongBrkCht = "https://www.finviz.com/screener.ashx?v=351&f=ind_stocksonly,sh_avgvol_o400,sh_price_o5,ta_averagetruerange_o1.5,ta_change_u2,ta_highlow20d_b0to3h,ta_highlow50d_b0to3h,ta_sma20_pa,ta_sma200_pa,ta_sma50_pa&ft=4&o=-change"
stkBrkCht = "https://www.finviz.com/screener.ashx?v=351&f=ind_stocksonly,sh_avgvol_o100,sh_curvol_o500,sh_price_o5,ta_change_u2,ta_changeopen_u3,ta_highlow52w_nh,ta_perf_dup&ft=4&o=-change"
etfBrkCht = "https://www.finviz.com/screener.ashx?v=351&f=ind_exchangetradedfund,sh_avgvol_o100,sh_curvol_o500,sh_price_o5,ta_changeopen_u3,ta_highlow52w_nh,ta_perf_dup&ft=4&o=-change"
stkShortSquz = "https://finviz.com/screener.ashx?v=351&f=ind_stocksonly,sh_avgvol_o50,sh_price_o10,sh_relvol_o1,sh_short_o15,ta_change_u2,ta_changeopen_u2,ta_highlow20d_nh,ta_sma50_sb20&ft=4&ta=0&o=perf4w"
stkShortBrkCht = "https://finviz.com/screener.ashx?v=111&f=cap_mid,sh_avgvol_o1000,sh_price_o7,ta_highlow20d_a0to3h,ta_sma20_pb,ta_sma200_pb,ta_sma50_pb&ft=4&o=-change"

# Kirk Daily Check
kirkWlIndexes = "https://finviz.com/screener.ashx?v=111&t=QQQ,IWC,OEF,IWM,SPY,MDY,DIA&o=-change"
kirkWlSectors = "https://finviz.com/screener.ashx?v=111&o=-change&t=XLC,%20XLK,%20XLY,%20XLRE,%20XLV,%20XLU,%20XLI,%20XLP,%20XLB,%20XLE,%20XLF"
kirkWlIndustries = "https://finviz.com/screener.ashx?v=111&o=-change&t=TAN,%20PBW,%20SOCL,%20XHB,%20ESPO,%20FDN,%20XRT,%20SKYY,%20AIEQ,%20HACK,%20WFH,%20ROBO,%20PBS,%20IGV,%20ARKK,%20BETZ,%20SMH,%20GDX,%20PEJ,%20IBB,%20CUT,%20IYR,%20PJP,%20IHI,%20PBJ,%20IHF,%20JETS,%20ITA,%20IYT,%20KRE,%20IGE,%20IGF,%20KIE,%20KBE,%20IYM,%20XOP,%20IAI,%20MJ,%20XME,%20OIH"
kirkWlFactors = "https://finviz.com/screener.ashx?v=111&o=-change&t=SPHB,SPGP,QUAL,SPVU,PKW,RPV,IVW,RPG,RWL,SPYD,RSP,SPY,SPVM,SPMV,NOBL,SPYV,SPLV,SPMO,SPHD"
kirkWlFixIncome = "https://finviz.com/screener.ashx?v=111&o=-change&t=TIP,%20EMB,%20HYG,%20IEF,%20IEI,%20ZROZ,%20TLT,%20SHY,%20AGG,%20MUB,%20TLH,%20IGOV,%20LQD"
kirkWlCurrencies = "https://finviz.com/screener.ashx?v=111&o=-change&t=FXE,%20FXB,%20FXF,%20FXA,%20CYB,%20FXC,%20FXY,%20CEW,%20UUP"
kirkWlCommodities = "https://finviz.com/screener.ashx?v=111&o=-change&t=LIT,%20SLV,%20WOOD,%20PPLT,%20GLD,%20UGA,%20BAL,%20MOO,%20VEGI,%20JJC,%20USO,%20NIB,%20PALL,%20DBC,%20URA,%20JO,%20SGG,%20WEAT,%20CORN,%20SOYB,%20UNG"
kirkWlGlobalMarkets = "https://finviz.com/screener.ashx?v=111&o=-change&t=FXI,%20EWN,%20EWO,%20EZA,%20EWD,%20IOO,%20EEM,%20EWT,%20TUR,%20EWG,%20SPY,%20EWY,%20EWA,%20VEU,%20EWH,%20EWL,%20GAL,%20EWK,%20FEZ,%20EFA,%20EPU,%20VEA,%20INDA,%20EWJ,%20EWU,%20EWQ,%20EWI,%20EWS,%20EPOL,%20EIDO,%20EUFN,%20VNM,%20ECH,%20EWC,%20FM,%20EIRL,%20THD,%20EWM,%20GREK,%20EWP,%20EPHE,%20EWW,%20ILF,%20RSX,%20EWZ,%20GXG"
kirkWlLeveraged = "https://finviz.com/screener.ashx?v=111&t=BRZU,CURE,DFEN,DPST,DRIP,DRN,DRV,DUSL,DUST,DZK,EDC,EDZ,ERX,ERY,EURL,FAS,FAZ,FNGD,FNGU,GUSH,INDL,JDST,JNUG,JPNL,KORU,LABD,LABU,LBJ,MEXX,MIDU,NAIL,NUGT,PILL,RETL,RUSL,SDOW,SMDD,SOXL,SOXS,SPXL,SPXS,SPXU,SQQQ,SRTY,TECL,TECS,TMF,TMV,TNA,TPOR,TQQQ,TTT,TYD,TYO,TZA,UBOT,UDOW,UMDD,UPRO,URTY,UTSL,YANG,YINN,&o=-change"
kirkWlEvryAwsome = "https://finviz.com/screener.ashx?v=111&t=UDOW,SPXL,MIDU,TNA,TQQQ,EDC,FNGU,&o=-change"

etfPerf1DUp = ""
etfPerf1DDw = ""
etfPerf1WUp = ""
etfPerf1WDw = ""
etfPerf1MUp = ""
etfPerf1MDw = ""
etfPerf1QUp = ""
etfPerf1QDw = ""
etfPerf1HUp = ""
etfPerf1HDw = ""
etfPerf1YUp = ""
etfPerf1YDw = ""
tkts_up_str = 'tkts_up_str'
showChartsLnk = "https://www.finviz.com/screener.ashx?v=351&t="

# Constants related to etfperf files
newDate = ''
const1D = '1D'
const1W = '1W'
const1M = '1M'
const1Q = '1Q'
const1H = '1H'
const1Y = '1Y'
midFileName = '_etfperf_'
extFileName = '.txt'
constList = [const1D,
             const1W,
             const1M,
             const1Q,
             const1H,
             const1Y]

# Constants related to update Excel files

TRADE_LOSS_LIST_PATH = r'C:\Users\jeron\Google Drive\trading\kirk\2022\active trading\tracking'
TRADE_LOSS_LIST_FILE = '2022_LossTradesAlert.xlsx'

WIN_NOT_COMP_LIST_PATH = r'C:\Users\jeron\Google Drive\trading\kirk\2022\active trading\tracking'
WIN_NOT_COMP_LIST_FILE = '2022_WonNotCompleteTradesAlert.xlsx'

WIN_LIST_PATH = r'C:\Users\jeron\Google Drive\trading\kirk\2022\active trading\tracking'
WIN_LIST_FILE = '2022_WonTrades.xlsx'

CAND_LIST_PATH = r'C:\Users\jeron\Google Drive\trading\kirk\2022\active trading'
CAND_LIST_FILE = '2022_KirkCandidatesManagementSpreadsheet.xlsx'

MONEYMGMT_SPSHT_PATH = r'C:\Users\jeron\Google Drive\trading\kirk\2022\active trading'
MONEYMGMT_SPSHT_FILE = '2022_MoneyManagementSpreadsheet.xlsx'
ORDERMGMT_SPSHT_FILE = '2022_OrderManagementSpreadsheet.xlsx'
MONTRMGMT_SPSHT_FILE = '2022_MonitorManagementSpreadsheet.xlsx'
TRACKERMT_SPSHT_FILE = '2022_ChangeTracker.xlsx'

TRADE_LOSS_LDN = TRADE_LOSS_LIST_PATH + '\\' + TRADE_LOSS_LIST_FILE
WIN_NOT_COMP_LDN = WIN_NOT_COMP_LIST_PATH + '\\' + WIN_NOT_COMP_LIST_FILE
WIN_LDN = WIN_LIST_PATH + '\\' + WIN_LIST_FILE
CAND_LIST_LDN = CAND_LIST_PATH + '\\' + CAND_LIST_FILE
MONEYMGMT_SPSHT_LDN = MONEYMGMT_SPSHT_PATH + '\\' + MONEYMGMT_SPSHT_FILE
ORDERMGMT_SPSHT_LDN = MONEYMGMT_SPSHT_PATH + '\\' + ORDERMGMT_SPSHT_FILE
MONTRMGMT_SPSHT_LDN = MONEYMGMT_SPSHT_PATH + '\\' + MONTRMGMT_SPSHT_FILE
TRACKERMT_SPSHT_LDN = MONEYMGMT_SPSHT_PATH + '\\' + TRACKERMT_SPSHT_FILE



# Constants related to buckets

BKT_PATH = r'C:\Users\jeron\Google Drive\trading\kirk\2022\listas'
BKT_COMMODITIES_FILE = '2022_POS_Commodities.xlsx'
BKT_CURRENCIES_FILE = '2022_POS_Currencies.xlsx'
BKT_FANGAM_FILE = '2022_POS_FANGAM.xlsx'
BKT_FIXEDINCOME_FILE = '2022_POS_Fixed_Income.xlsx'
BKT_FOREIGNMARKETS_FILE = '2022_POS_Foreign_Markets.xlsx'
BKT_INDUSTRIES_FILE = '2022_POS_Industries.xlsx'
BKT_MEGATRENDS_FILE = '2022_POS_Megatrends.xlsx'
BKT_LEVERAGED_FILE = '2022_POS_Other.xlsx'
BKT_SECTORS_FILE = '2022_POS_Sectors.xlsx'
BKT_STYLES_FILE = '2022_POS_Styles.xlsx'
BKT_USMARKETS_FILE = '2022_POS_US_Markets.xlsx'
BKT_STOCKS_FILE = '2022_POS_Weekly.xlsx'
BKT_LISTS_FILE = '2022_ListasTrack.xlsx'

BKT_COMMODITIES_LDN = BKT_PATH + '\\' + BKT_COMMODITIES_FILE
BKT_CURRENCIES_LDN = BKT_PATH + '\\' + BKT_CURRENCIES_FILE
BKT_FANGAM_LDN = BKT_PATH + '\\' + BKT_FANGAM_FILE
BKT_FIXEDINCOME_LDN = BKT_PATH + '\\' + BKT_FIXEDINCOME_FILE
BKT_FOREIGNMARKETS_LDN = BKT_PATH + '\\' + BKT_FOREIGNMARKETS_FILE
BKT_INDUSTRIES_LDN = BKT_PATH + '\\' + BKT_INDUSTRIES_FILE
BKT_MEGATRENDS_LDN = BKT_PATH + '\\' + BKT_MEGATRENDS_FILE
BKT_LEVERAGED_LDN = BKT_PATH + '\\' + BKT_LEVERAGED_FILE
BKT_SECTORS_LDN = BKT_PATH + '\\' + BKT_SECTORS_FILE
BKT_STYLES_LDN = BKT_PATH + '\\' + BKT_STYLES_FILE
BKT_USMARKETS_LDN = BKT_PATH + '\\' + BKT_USMARKETS_FILE
BKT_STOCKS_LDN = BKT_PATH + '\\' + BKT_STOCKS_FILE
BKT_LISTS_LDN = BKT_PATH + '\\' + BKT_LISTS_FILE

# GUI
sg.theme('BluePurple')

layout = [[sg.Text('*** Conexion DB & ETF Performance ***')],
          [sg.Button(buttonConnectDb),sg.Button(buttonReadDb),sg.Button(buttonReadPicFile),
           sg.Button(buttonWritePicDb),sg.Button(buttonExec)], 
          [sg.Text('*** Posiciones Abiertas ***')],
          [sg.Button(buttonShowCharts),sg.Button(buttonMoneyManagementSpsht),sg.Button(buttonOpenOrderManagementSpsht),
           sg.Button(buttonOpenMonitorManagementSpsht),sg.Button(buttonOpenChangeTrackerSpsht)],
          [sg.Text('*** Supporting Excel Files ***')],
          [sg.Button(buttonOpenLostTradesTracker), sg.Button(buttonOpenWonNotCompletedTracker),
           sg.Button(buttonOpenWonCompletedTracker),sg.Button(buttonOpenCandidatesTracker)],
          [sg.Text('*** Buckets Charts ***')],
          [sg.Button(buttonOpenChartsScreen)],
          [sg.Text('*** Buckets Excel Files ***')],
          [sg.Button(buttonBktCommodities), sg.Button(buttonBktCurrencies), sg.Button(buttonBktFANGAM),
           sg.Button(buttonBktFixedIncome), sg.Button(buttonBktForeignMarktes), sg.Button(buttonBktIndustries)],
          [sg.Button(buttonBktMegatrends), sg.Button(buttonBktLeveraged), sg.Button(buttonBktSectors),
           sg.Button(buttonBktStyles), sg.Button(buttonBktUsMarkets), sg.Button(buttonBktStocks),sg.Button(buttonOpenBktListSpsht)],
          [sg.Text('*** Sectors Performance ***')], 
          [sg.Button('Sectors Daily'), sg.Button('Sectors 1W'), sg.Button('Sectors 4W'),  
           sg.Button('Sectors 13W'), sg.Button('Sectors 26W'), sg.Button('Sectors 52W'),  
           sg.Button('Sectors YTD')],\
          [sg.Text('*** Kirk Watchlist ***')],
          [sg.Button('indexes'), sg.InputText(key='kirkWlIndexes'),sg.Button('sectors'), sg.InputText(key='kirkWlSectors')],
          [sg.Button('industries'), sg.InputText(key='kirkWlIndustries'),sg.Button('factors'), sg.InputText(key='kirkWlFactors')],
          [sg.Button('fixed income'), sg.InputText(key='kirkWlFixIncome'),sg.Button('currencies'), sg.InputText(key='kirkWlCurrencies')],
          [sg.Button('commodities'), sg.InputText(key='kirkWlCommodities'),sg.Button('global markets'), sg.InputText(key='kirkWlGlobalMarkets')],
          [sg.Button('leveraged'), sg.InputText(key='kirkWlLeveraged'),sg.Button('AwesomePort'), sg.InputText(key='kirkWlEvryAwsome')],
          [sg.Button('ETF Perf Daily'), sg.InputText(key='etfPerfDaily'),sg.Button('ETF Perf Weekly'), sg.InputText(key='etfPerfWeekly')],
          [sg.Text('*** Scans ***')],
          [sg.Button('New High ETF'), sg.InputText(key='etfNewHighCht'),sg.Button('New High STK'), sg.InputText(key='stkNewHighCht')],
          [sg.Button('Simple Breakout Scan ETF'), sg.InputText(key='etfBrkCht'),sg.Button('Simple Breakout Scan STK'), sg.InputText(key='stkBrkCht')],
          [sg.Button('Long Breakout Setup ETF'), sg.InputText(key='etfLongBrkCht'),sg.Button('Long Breakout Setup STK'), sg.InputText(key='stkLongBrkCht')],
          [sg.Button('FATGANMSN'), sg.InputText(key='fatganmsn'), sg.Button('Major News'), sg.InputText(key='majorNewsCht')],
          [sg.Button('Most Shorted Stocks'), sg.InputText(key='stkShortSquz'),sg.Button('Break Down Setups'), sg.InputText(key='stkShortBrkCht')],
          [sg.Text('*** Assign Bucket ***')],
          [sg.Button(buttonProcess), sg.InputText(key='possibleCand')],
          [sg.Text('*** Generate Candidates ***')],
          [ sg.Button(buttonChkPlaysLong), sg.Button(buttonChkPlaysShort), sg.Button(buttonChkList)],
          [sg.Text('******************')],         
          [sg.Button('Exit')]]

# Main Program V2

# Open connection to db
window = sg.Window('TorolGui', layout)
try:
    while True:  # Event Loop
        event, values = window.read()

        if event == 'Exit':
            break
    
        if event == buttonConnectDb:
            sql_conn = dbh.ConnectSQLDb(kc.db_prefix, kc.db_struc_etf)
    
        if event == buttonChkList:
            result = 1
            result = tu.CheckEtfsLists(tradeType='Long',tradeFlag='LONG')
            if result == 0:
                print('finished')
        
        if event == buttonChkPlaysLong:
            result = 1
            result = tu.GenerateCandidates(tradeType='long')
            if result == 0:
                print('finished')
        
        if event == buttonChkPlaysShort:
            result = 1
            result = tu.GenerateCandidates(tradeType='short')
            if result == 0:
                print('finished')
           
        if event == buttonShowCharts:
            print('*** Open Charts Positions Open ***')
            list_tktOpen = up.GetTktPositionsOpen(pathFile=kc.tablePath,nameFile=kc.tableFile,nameSheet=kc.tableSheet)
            if len(list_tktOpen) > 0:
                print(showChartsLnk + str(list_tktOpen))
                delim = ','
                openweb("chrome", [showChartsLnk + delim.join(list_tktOpen)])
        
        if event == buttonOpenChartsScreen:
            print('*** Open Charts Screen ***')
            etf_df = scetf.ReadSerialEtfScreen(kc.fileNamePickle, kc.testPath)
            for item in buttonChtList:
                openweb("chrome", [chartsArgumnets(item)])

        if event == buttonOpenLostTradesTracker:
            up.OpenExcelSupportFile(excelFile=TRADE_LOSS_LDN)
            print('*** Excel Update ***' + ' ' + buttonOpenLostTradesTracker)

        if event == buttonOpenWonNotCompletedTracker:
            up.OpenExcelSupportFile(excelFile=WIN_NOT_COMP_LDN)
            print('*** Excel Update ***' + ' ' + buttonOpenWonNotCompletedTracker)

        if event == buttonOpenWonCompletedTracker:
            up.OpenExcelSupportFile(excelFile=WIN_LDN)
            print('*** Excel Update ***' + ' ' + buttonOpenWonCompletedTracker)

        if event == buttonOpenOrderManagementSpsht:
            up.OpenExcelSupportFile(excelFile=ORDERMGMT_SPSHT_LDN)
            print('*** Excel Update ***' + ' ' + buttonOpenOrderManagementSpsht)

        if event == buttonOpenBktListSpsht:
            up.OpenExcelSupportFile(excelFile=BKT_LISTS_LDN)
            print('*** Excel Update ***' + ' ' + buttonOpenBktListSpsht)

        if event == buttonOpenCandidatesTracker:
            up.OpenExcelSupportFile(excelFile=CAND_LIST_LDN)
            print('*** Excel Update ***' + ' ' + buttonOpenCandidatesTracker)
        
        if event == buttonMoneyManagementSpsht:
            up.OpenExcelSupportFile(excelFile=MONEYMGMT_SPSHT_LDN)
            print('*** OpenExcelSupportFile ***' + ' ' + buttonMoneyManagementSpsht)            

        if event == buttonOpenMonitorManagementSpsht:
            up.OpenExcelSupportFile(excelFile=MONTRMGMT_SPSHT_LDN)
            print('*** OpenExcelSupportFile ***' + ' ' + buttonOpenMonitorManagementSpsht)

        if event == buttonOpenChangeTrackerSpsht:
            up.OpenExcelSupportFile(excelFile=TRACKERMT_SPSHT_LDN)
            print('*** OpenExcelSupportFile ***' + ' ' + buttonOpenChangeTrackerSpsht)

        if event == buttonBktCommodities:
            up.OpenExcelSupportFile(excelFile=BKT_COMMODITIES_LDN)
            print('*** OpenExcelSupportFile ***' + ' ' + buttonBktCommodities)

        if event == buttonBktCurrencies:
            up.OpenExcelSupportFile(excelFile=BKT_CURRENCIES_LDN)
            print('*** OpenExcelSupportFile ***' + ' ' + buttonBktCurrencies)

        if event == buttonBktFANGAM:
            up.OpenExcelSupportFile(excelFile=BKT_FANGAM_LDN)
            print('*** OpenExcelSupportFile ***' + ' ' + buttonBktFANGAM)

        if event == buttonBktFixedIncome:
            up.OpenExcelSupportFile(excelFile=BKT_FIXEDINCOME_LDN)
            print('*** OpenExcelSupportFile ***' + ' ' + buttonBktFixedIncome)

        if event == buttonBktForeignMarktes:
            up.OpenExcelSupportFile(excelFile=BKT_FOREIGNMARKETS_LDN)
            print('*** OpenExcelSupportFile ***' + ' ' + buttonBktForeignMarktes)

        if event == buttonBktIndustries:
            up.OpenExcelSupportFile(excelFile=BKT_INDUSTRIES_LDN)
            print('*** OpenExcelSupportFile ***' + ' ' + buttonBktIndustries)

        if event == buttonBktMegatrends:
            up.OpenExcelSupportFile(excelFile=BKT_MEGATRENDS_LDN)
            print('*** OpenExcelSupportFile ***' + ' ' + buttonBktMegatrends)

        if event == buttonBktLeveraged:
            up.OpenExcelSupportFile(excelFile=BKT_LEVERAGED_LDN)
            print('*** OpenExcelSupportFile ***' + ' ' + buttonBktLeveraged)

        if event == buttonBktSectors:
            up.OpenExcelSupportFile(excelFile=BKT_SECTORS_LDN)
            print('*** OpenExcelSupportFile ***' + ' ' + buttonBktSectors)

        if event == buttonBktStyles:
            up.OpenExcelSupportFile(excelFile=BKT_STYLES_LDN)
            print('*** OpenExcelSupportFile ***' + ' ' + buttonBktStyles)

        if event == buttonBktUsMarkets:
            up.OpenExcelSupportFile(excelFile=BKT_USMARKETS_LDN)
            print('*** OpenExcelSupportFile ***' + ' ' + buttonBktUsMarkets)

        if event == buttonBktStocks:
            up.OpenExcelSupportFile(excelFile=BKT_STOCKS_LDN)
            print('*** OpenExcelSupportFile ***' + ' ' + buttonBktStocks)

        if event in buttonChtList:
            openweb("chrome", [chartsArgumnets(event)])
        
        if event == buttonReadDb:
            etf_df = dbh.ReadSQLTable(sql_conn, kc.db_table_etf)
            etf_df = scetf.ReadSerialEtfScreen(kc.fileNamePickle, kc.testPath)
            etfPerf1DUp, etfPerf1DDw = scetf.EtfPrintTopBottom(etf_df, kc.topNumber, kc.const1D)
            etfPerf1WUp, etfPerf1WDw = scetf.EtfPrintTopBottom(etf_df, kc.topNumber, kc.const1W)
            etfPerf1MUp, etfPerf1MDw = scetf.EtfPrintTopBottom(etf_df, kc.topNumber, kc.const1M)
            etfPerf1QUp, etfPerf1QDw = scetf.EtfPrintTopBottom(etf_df, kc.topNumber, kc.const1Q)
            etfPerf1HUp, etfPerf1HDw = scetf.EtfPrintTopBottom(etf_df, kc.topNumber, kc.const1H)
            etfPerf1YUp, etfPerf1YDw = scetf.EtfPrintTopBottom(etf_df, kc.topNumber, kc.const1Y)
            print('*** ' + event + ' ***')
            print(etf_df)
    
        if event == buttonReadPicFile:
            etf_df = scetf.ReadSerialEtfScreen(kc.fileNamePickle, kc.testPath)
            etfPerf1DUp, etfPerf1DDw = scetf.EtfPrintTopBottom(etf_df, kc.topNumber, kc.const1D)
            etfPerf1WUp, etfPerf1WDw = scetf.EtfPrintTopBottom(etf_df, kc.topNumber, kc.const1W)
            etfPerf1MUp, etfPerf1MDw = scetf.EtfPrintTopBottom(etf_df, kc.topNumber, kc.const1M)
            etfPerf1QUp, etfPerf1QDw = scetf.EtfPrintTopBottom(etf_df, kc.topNumber, kc.const1Q)
            etfPerf1HUp, etfPerf1HDw = scetf.EtfPrintTopBottom(etf_df, kc.topNumber, kc.const1H)
            etfPerf1YUp, etfPerf1YDw = scetf.EtfPrintTopBottom(etf_df, kc.topNumber, kc.const1Y)
            print('*** ' + event + ' ***')
            print(etf_df)
    
        if event == buttonWritePicDb:
            etf_df = scetf.ReadSerialEtfScreen(kc.fileNamePickle, kc.testPath)
            dbh.WriteSQLTable(etf_df, sql_conn, kc.db_table_etf)
            print('*** ' + event + ' ***')
            print(etf_df)
    
        if event == buttonExec:
            etf_df = dbh.ReadSQLTable(sql_conn, kc.db_table_etf)
            sg.Print(size=sectorsPerfWindow, do_not_reroute_stdout=False)
            print('*** ETF ***')
            etfPerf1DUp, etfPerf1DDw = scetf.EtfPrintTopBottom(etf_df, kc.topNumber, kc.const1D)
            etfPerf1WUp, etfPerf1WDw = scetf.EtfPrintTopBottom(etf_df, kc.topNumber, kc.const1W)
            etfPerf1MUp, etfPerf1MDw = scetf.EtfPrintTopBottom(etf_df, kc.topNumber, kc.const1M)
            etfPerf1QUp, etfPerf1QDw = scetf.EtfPrintTopBottom(etf_df, kc.topNumber, kc.const1Q)
            etfPerf1HUp, etfPerf1HDw = scetf.EtfPrintTopBottom(etf_df, kc.topNumber, kc.const1H)
            etfPerf1YUp, etfPerf1YDw = scetf.EtfPrintTopBottom(etf_df, kc.topNumber, kc.const1Y)
            sys.stdout = sys.__stdout__
                
        if event == 'Execute_to_fix':
            fileinfo = values['-IN-']
            print(type(fileinfo))
            fileinfoList = fileinfo.split("/")
            if len(fileinfoList) > 0:
                newDate = fileinfoList[len(fileinfoList) - 1].split("_")[0]
                print('this is new date')
                print(newDate)
    
                os.chdir(script_path)
            
                for script_file in script_list:
                    print('BEGIN Filename is ' + script_file)
                    f = open(script_file,"r")
                    lines = f.readlines()
                    f.close()
                    for i, line in enumerate(lines):
                        if(line.startswith(lineStartToChange1) or line.startswith(lineStartToChange2)):
                            line_list = line.split("=")
                            if line.startswith(lineStartToChange1):
                                print("line 1 before" + line_list[1])
                                newString = newDate
                                olString = line_list[1][4:12]
                                line_list[1] = line_list[1].replace(olString, newString)
                                print("line 1 after" + line_list[1])
                            if line.startswith(lineStartToChange2):
                                newString = newDate[0:4]
                                olString = line_list[2][2:6]
                                line_list[2] = line_list[2].replace(olString, newString)
                            lines[i] =  "=".join(line_list)
                    f = open(script_file, "w")
                    f.write("".join(lines))
                    f.close()
                    print('END Filename is ' + script_file)
                
                # Execute the file
                for script_file in script_list:
                    os.system('python ' + script_file)
    
        # Performance printing on Windows
        if (event in buttonSecList):
            paramList = ScreenerArguments(event)
            print(paramList)
            if len(paramList) > 1:
                screenResult = TktScreeenTable(sectorsTktList, paramList[0], paramList[1])
                sg.Print(size=sectorsPerfWindow, do_not_reroute_stdout=False)
                print('*** ' + event.upper()  + ' ***')
                print(' ')
                print(screenResult)
                # set output back to console
                sys.stdout = sys.__stdout__
        else:
            if (event == buttonProcess):
                for textTkts in textBoxList:
                    if (len(values[textTkts]) > 0):
                        listCand = candList(values[textTkts])
                        if (len(listCand) > 0):
                            if (textTkts.startswith(etfPref)):
                                etfSet.update(listCand)
                            else:
                                stkSet.update(listCand)
                candString = ''
                if((len(etfSet) > 0) | (len(stkSet) > 0)):
                    totalSet = etfSet.union(stkSet)
                    finalCand_lst = checkOpenPositions(list(totalSet))
                    candString = ','.join(finalCand_lst)
                    window['possibleCand'].update(candString)
                    dcan.AddRowCandToDb(sql_conn, kc.dbCandTable, datetime.date.today(), candString)
                    print(candString)
                # send output to window
                sg.Print(size=sectorsPerfWindow, do_not_reroute_stdout=False)
                print('*** TKTS LIST ***')
                print(candString)
                print('*** SCREENS ***')
                for textTkts in textBoxList:
                    print(textTkts + ': '  + values[textTkts])
                print("etfSet" + ' ' + str(etfSet))
                print("stkSet" + ' ' + str(stkSet))
                print('******')
                print(' ')
                print('*** CANDIDATES  ***')
                printBuckets(etfSet, stkSet, listPath, fileList, sheetList)
                # set output back to console
                sys.stdout = sys.__stdout__
                initializeSets()
except:
    print('exception generated')
    e = sys.exc_info()[0]
    print('Exception ' + e)
    print('last event ' + event)
    pass


window.close()
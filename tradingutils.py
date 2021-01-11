import pandas as pd
import datetime as dt
import yfinance as yf
import kirkconstants as kc
import updatemms as upm

# This function gets the bucket list value for each tkt
def GetBucket(tkt, dfBucket):
    print("This is a test")
    
# This function changes Bucket into an easier dataframe
def TransFormBucket(dfBucket, colname):
    listBuckets = dfBucket.columns.to_list()
    df1 = pd.DataFrame(columns = [colname, 'bucket'])
    for item in listBuckets:
        df2 = pd.DataFrame(dfBucket[item].dropna(how='all').to_list(),columns = [colname])
        df2['bucket'] = item
        df1 = pd.concat([df1, df2], ignore_index=True)
    return df1

# This function get trading data for a TKT from 
def GetData(symbol, start='2000-01-01', interval='1d', end=None):
    data = yf.download(symbol, start=start, end=end, interval=interval, auto_adjust=True)
    return data

# This function get trading data for a tkt list
def GetDataM(listado, start='2000-01-01', interval='1d', end=None, version=1):
    data = yf.download(listado, start=start, end=end, interval=interval, auto_adjust=True)
    if(version != 1):
        return data
    else:
        return data.swaplevel(i=1, j=0, axis=1)

# This function get K%
def StochOscK(pd_tkt, n=14):
    data = ((pd_tkt['Close'] - pd_tkt['Low'].rolling(n).min()) / (pd_tkt['High'].rolling(n).max() - pd_tkt['Low'].rolling(n).min())) * 100
    return data

# This function get D% assuming in pd_tkt there is a K% value available
def StochOscD(pd_tkt, n=14, m=3):
    data = pd_tkt['%K'].rolling(m).mean()
    return data

# This function calculate EmaAvg
def EmaAvg(pd_tkt, n):
    return pd_tkt['Close'].ewm(span=n).mean()

# This function calculate FastEma (5)
def FastEma(pd_tkt, fastInt=5):
    return EmaAvg(pd_tkt, fastInt)

# This function calculate FastEma (13)
def SlowEma(pd_tkt, slowInt=13):
    return EmaAvg(pd_tkt, slowInt)

# This function calculate Single Moving Average (20)
def SingleMa(pd_tkt, n=20):
    return pd_tkt['Close'].rolling(n).mean()
    
# This procedure generates Trading Table Data with Tech Indicators
def AddTradingIndToData(dfTradeEvalLong):
    #get data from multiple tkts from yf
    listTradeEval = dfTradeEvalLong['tkt'].tolist()
    dataTradeEval = GetDataM(listTradeEval)
    
    # get uniques tkts
    tktList = list(set(listTradeEval))
    #add indicators to dataTradeEval
    for t in tktList:
        dataTradeEval[(t,'Close')]
        dataTradeEval[(t,'sma_20')] = SingleMa(dataTradeEval[(t)], n=20)
        dataTradeEval[(t,'ema_5')] = FastEma(dataTradeEval[(t)])
        dataTradeEval[(t,'ema_13')] = SlowEma(dataTradeEval[(t)])
        dataTradeEval[(t,'%K')] = StochOscK(dataTradeEval[(t)])
        dataTradeEval[(t,'%D')] = StochOscD(dataTradeEval[(t)])
    return dataTradeEval

# This procedure generates a table with the most recent data tail(1) to
# the trading data from yfinance and also adds the tkt so it can be 
# merged with Kirk Table
def TailTradingDataWithTkt(dataTradeEval):
    #most recent data
    dfexp = dataTradeEval.tail(1)
    
    dfexp.columns.tolist()
    tktSet = set()
    for t in (dfexp.columns.tolist()):
        tktSet.add(t[0])
    tktList = list(tktSet)
    
    dft = pd.DataFrame()
    for t in tktList:
        val = dfexp[(t)].values.tolist()
        col = dfexp[(t)].columns.tolist()
        pdtest = pd.DataFrame(data = val, columns = col)
        pdtest['tkt'] = t
        dft = pd.concat([dft, pdtest], ignore_index=True)
    return dft

 
def GetActiveTradeList(actTradesPath, actTradesFile, actTradestSheet):
    # Excel info
    code_col = kc.code_col
    date_col = kc.date_col
    price_col = kc.price_col
    start_row = kc.start_row
    
    # Years to be selected
    year_prefix = kc.year_prefix
    
    tkt = set()
    workbook = upm.ReadWorkbook(actTradesPath, actTradesFile)
    trade_log = workbook[actTradestSheet]

    for row in trade_log.iter_rows(min_row=start_row, 
                                   min_col=code_col,
                                   max_col=price_col):
        cell_tkt = row[code_col -1]
        if cell_tkt.value is None:
            break
        else:
            cell_date = row[date_col -1]
            if (cell_date.value.year == year_prefix):
                print(str(cell_tkt.value))
                tkt.add(cell_tkt.value)
    tkt_list = sorted(list(tkt))
    return tkt_list


def UniqueTradeEvalList(dfTradeEvalLong, activeTkt_list):
    ''' This function returns a df with tkts left 
        after removing active positions that come in activeTkt_list'''
    indexToDrop = dfTradeEvalLong[dfTradeEvalLong['tkt'].isin(activeTkt_list)].index
    dfTradeEvalLong2 = dfTradeEvalLong.drop(index = indexToDrop)
    
    return dfTradeEvalLong2

def ExecuteCode(tradeType):
    
    print('Begin - ExecuteOldCode')
    
    # File information
    tablePath = kc.candPath
    tableSheet = kc.candSheet
    tableFile = kc.candFile
    
    bucketPath = kc.bucketPath
    bucketFile = kc.bucketFile
    bucketSheet = kc.bucketSheet
    balanceSheet = kc.balanceSheet
    
    actTradesPath = kc.actTradesPath
    actTradesFile = kc.actTradesFile
    actTradestSheet = kc.actTradestSheet
    
    posTradesPath = kc.posTradesPath
    posTradeRawFileSfx = kc.posTradeRawFileSfx
    posTradeFinalFileSfx = kc.posTradeFinalFileSfx

    # Get Active Trades
    activeTkt_list = GetActiveTradeList(actTradesPath, actTradesFile, actTradestSheet)
    
    # reading original table
    dfTrading = upm.OpenExcelFile(tablePath, tableFile, tableSheet)
    
    # read bucket & balance files
    dfBucket = upm.OpenExcelFile(bucketPath, bucketFile, bucketSheet)
    dfBalance = upm.OpenExcelFile(bucketPath, bucketFile, balanceSheet)
    
    # transform buckets in a more manageable format
    dfBucketT = TransFormBucket(dfBucket, 'tkt')
    dfBalanceT = TransFormBucket(dfBalance, 'balance')
    
    # droping msft_tkt
    dfTbl = dfTrading.drop(columns=['msft_tkt'])
    # rename column
    dfTbl.rename(columns = {'date':'old_date'}, inplace = True)
    # format date
    dfTbl['date'] = pd.to_datetime(dfTbl['old_date'].astype(str), format='%Y%m%d')
    dfTbl = dfTbl.drop(columns=['old_date'])
    
    # select specific year
    # dfTbl = dfTbl[dfTbl['date'].dt.year == year_prefix]
     
    dfTbl = dfTbl.loc[((dfTbl['p1'].isin(['m'])) | \
                       (dfTbl['p2'].isin(['m'])) | \
                       (dfTbl['p3'].isin(['m'])) | \
                       (dfTbl['p4'].isin(['m'])) | \
                       (dfTbl['p5'].isin(['m']))),:].copy()

    # Merge Kirk Candidate Table without filtering to Bucket Allocation file
    dfTradeEval = pd.merge(left=dfTbl, right=dfBucketT, how='left', left_on='tkt', right_on='tkt')
    dfTradeEval.bucket = dfTradeEval.bucket.fillna(value='Weekly')
    dfTradeEval = pd.merge(left=dfTradeEval, right=dfBalanceT, how='left', left_on='bucket', right_on='bucket')

    dfTradeEvalLong = dfTradeEval[(dfTradeEval['tipo'].str.lower() == tradeType) & (dfTradeEval['flag'].str.lower() == tradeType)]
    idx_to_drop = dfTradeEvalLong[(dfTradeEvalLong['long_above'].isnull().values == True) | (dfTradeEvalLong['short_below'].isnull().values == True)].index
    
    # Evaluate Long Trades
    dfTradeEvalLong = dfTradeEvalLong.drop(idx_to_drop).copy()
    dfTradeEvalLong2 = UniqueTradeEvalList(dfTradeEvalLong, activeTkt_list)
    dataTradeEval = AddTradingIndToData(dfTradeEvalLong2)
    dfTechToMerge = TailTradingDataWithTkt(dataTradeEval)
    dfTradeEvalLongPre = pd.merge(left=dfTradeEvalLong2, right=dfTechToMerge, how='left', left_on='tkt', right_on='tkt')

    condition = (dfTradeEvalLongPre.Close > dfTradeEvalLongPre.init_price) & \
                (dfTradeEvalLongPre.Close > dfTradeEvalLongPre.ema_5) & \
                (dfTradeEvalLongPre.ema_5 > dfTradeEvalLongPre.ema_13) & \
                (dfTradeEvalLongPre.ema_13 > dfTradeEvalLongPre.sma_20) & \
                (dfTradeEvalLongPre['%K'] > 45) & \
                (dfTradeEvalLongPre['balance'] > 0)
                
    dfPossibleTrades = dfTradeEvalLongPre.loc[condition].sort_values('%K').copy()

    risk = kc.risk
    commision = kc.commision
    stoploss_perc = kc.stoploss_perc
    rwd_rsk_factor = kc.rwd_rsk_factor
    
    dfPossibleTrades['stop_loss'] = dfPossibleTrades['Close'] * (1 - (stoploss_perc/100))
    dfPossibleTrades['target'] = dfPossibleTrades[["t1","t2","t3","t4","t5"]].max(axis=1)
    dfPossibleTrades['risk'] = risk
    dfPossibleTrades['R'] = ((dfPossibleTrades['balance'] * dfPossibleTrades['risk'])/100) + commision
    
    dfPossibleTrades['shares'] = dfPossibleTrades['R']/(dfPossibleTrades['Close'] - dfPossibleTrades['stop_loss'])
    dfPossibleTrades['rsk'] = (dfPossibleTrades['stop_loss'] - dfPossibleTrades['Close']) * dfPossibleTrades['shares']
    dfPossibleTrades['rwd'] = ((dfPossibleTrades['target'] - dfPossibleTrades['Close']) * dfPossibleTrades['shares']) - commision
    dfPossibleTrades['rwd_rsk_ratio'] = abs(dfPossibleTrades['rwd']/dfPossibleTrades['rsk'])
    dfPossibleTrades[['bucket','R','shares', 'rwd_rsk_ratio']]

    # Writing to csv all possible trades   
    PossibleTradesToFile(dfPossibleTrades, posTradesPath, posTradeRawFileSfx, tradeType)
    
    # Trades candidates with rs/rw filter
    condition = dfPossibleTrades['rwd_rsk_ratio'] > rwd_rsk_factor
    dfPossibleTradesFinal = dfPossibleTrades.loc[condition].copy()

    # Writing to csv only trades with valid rs/rw    
    PossibleTradesToFile(dfPossibleTradesFinal, posTradesPath, posTradeFinalFileSfx, tradeType)  
    print('End - ExecuteOldCode')

def PossibleTradesToFile(dfCandidates, tradePath, tradeFile, tradeType):
    ''' This function takes a dataframe with possible candidates and a file suffix and writes it to a csv file)
    '''
    print('Begin - PossibleTradesToFile')
    fileSuffix = '_' + tradeFile + '_' + tradeType + '.csv'
    posTradeFile = str(dt.date.today()).replace('-','') + fileSuffix
    upm.ExportDfToCsv(dfCandidates, tradePath, posTradeFile)
    print('End - PossibleTradesToFile')


def CheckEtfsLists(tradeType='Long',tradeFlag='LONG'):
    print('Begin CheckEtfsLists')

    # File information
    bucketPath = kc.bucketPath
    bucketFile = kc.bucketFile
    bucketSheet = kc.bucketSheet
    balanceSheet = kc.balanceSheet

    etfChkPath = kc.etfChkPath
    etfChkFileSfx = kc.etfChkFileSfx
    
    # read bucket & balance files
    dfBucket = upm.OpenExcelFile(bucketPath, bucketFile, bucketSheet)
    
    # transform buckets in a more manageable format
    dfBucketT = TransFormBucket(dfBucket, 'tkt')
    print('End CheckEtfsLists')
    return 0

def GenerateCandidates(tradeType='long'):
    print('Begin GenerateCandidates')
    ExecuteCode(tradeType)
    print('End GenerateCandidates')
    return 0

def main():
    # Formatting pandas to have 2 decimal points
    pd.options.display.float_format = "{:,.2f}".format
    result = GenerateCandidates()
    print(str(result))

if __name__ == "__main__":
    try:
        main()
    except SystemExit as e:
        print('Error Exception triggered')

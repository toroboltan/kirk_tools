'''
Created on Sep 26, 2019

@author: CEVDEA
'''
from winerror import ERROR_DS_NO_REQUESTED_ATTS_FOUND
from google.protobuf.internal._parameterized import parameters
'''
    Convert to float a string value
'''

import os
import re
import pandas as pd
from finviz.screener import Screener

cons_Rtn1d = '1d'
cons_formatTxt = 'txt'
cons_formatHtml = 'html'

def float_or_na(value):
    return float(value) if value.upper() != 'N/A' else None

def tktFileReader(filePath_s, fileName_s, fileFormat_s):
    #local constant
    STRINGNOTFOUND_N1 = -1
    headerLabel_s = 'Name'
    footerLabel_s = 'symbols listed'
    middleLabel_s = 'Sort Asc'
    #variables
    tktLines_L = []
    flagBegin_B = False
    flagMiddle_B = False
    flagEnd_B = False
    
    os.chdir(filePath_s)
    
    if(fileFormat_s == cons_formatTxt):
        with open(fileName_s) as filehandle:
            for lineFile_s in filehandle:
                if not flagBegin_B and lineFile_s.find(headerLabel_s) != STRINGNOTFOUND_N1:
                    flagBegin_B = True
                if flagBegin_B and lineFile_s.find(middleLabel_s) != STRINGNOTFOUND_N1:
                    flagMiddle_B = True
                    continue
                if not flagEnd_B and lineFile_s.find(footerLabel_s) != STRINGNOTFOUND_N1:
                    flagEnd_B = True
                if(flagBegin_B and flagMiddle_B and not flagEnd_B):
                    tktLines_L.append(lineFile_s)
    elif(fileFormat_s == cons_formatHtml):
        print('not implemented yet')
    
    return(tktLines_L)

def tktTxtLineParser(line_s, lineFormat_s):
    if(lineFormat_s == cons_formatTxt):
        tktParsed_L = re.split(r'\t+', line_s.rstrip('\t'))
    elif(lineFormat_s == cons_formatHtml):
        print('not implemented yet') 
    return(tktParsed_L)

'''
    This function prints Top/Bottom numberToPrintInt from tktList daily list
    It is assumed tktList values are sorted based on daily return
'''
def tktPrintTopBottomPerformers(tktList, numberToPrintInt):
    lenTktList = len(tktList)
    if(lenTktList > 0) and (lenTktList >= numberToPrintInt) and (numberToPrintInt):
        print('*** Print ETF UP (' + str(numberToPrintInt) + ') ***')
        for i in range(0,numberToPrintInt + 1):
            print(tktList[i].tktPrintSymbol())
        print('*** Print ETF DOWN (' + str(numberToPrintInt) + ') ***')
        for i in range(0,numberToPrintInt + 1):
            print(tktList[lenTktList-1 - i].tktPrintSymbol())


'''
    This function return a list of elements to be used as input for a pandas dataframe
    Each element is a list with all fields related to tktEtfScreen class
'''
def tktParserFromTktListToDataframeList(tktList):
    list_input_dataframe = []

    for i in range(0, len(tktList)):
        list_tkt_element = []
        list_tkt_element.append(tktList[i].nameTkt_s)
        list_tkt_element.append(tktList[i].symbolTkt_s)
        list_tkt_element.append(tktList[i].rsfTkt_f)
        list_tkt_element.append(tktList[i].priceTkt)
        list_tkt_element.append((float_or_na(tktList[i].rtn1dTkt_f)))
        list_tkt_element.append((float_or_na(tktList[i].rtn5dTkt_f)))
        list_tkt_element.append((float_or_na(tktList[i].rtn1mTkt_f)))
        list_tkt_element.append((float_or_na(tktList[i].rtn3mTkt_f)))
        list_tkt_element.append((float_or_na(tktList[i].rtn6mTkt_f)))        
        list_tkt_element.append((float_or_na(tktList[i].rtn1yTkt_f)))
        list_tkt_element.append(tktList[i].vol21Tkt_s)
        list_input_dataframe.append(list_tkt_element)
    
    return list_input_dataframe

'''
    This function prints Top/Bottom numberToPrintInt from a pandas 
    dataframe based on timeRange 
'''
def tktDfPrintTopBottom(tkt_dataframe, numberToPrintInt, timeRange, filePrefix, outputDir):
    #     Name    Symbol    RSf    Rtn-1d    Rtn-5d    Rtn-1mo    Rtn-3mo    Rtn-6mo    Rtn-1yr    $vol-21
    lenTktList = len(tkt_dataframe.index)
    if(lenTktList > 0) and (lenTktList >= numberToPrintInt) and (numberToPrintInt):
        final_up_df = pd.DataFrame()
        final_dw_df = pd.DataFrame()
        columnVal = ''
        if timeRange == '1D':
            final_up_df = tkt_dataframe[tkt_dataframe['Rtn-1d'] > 0.0].sort_values(by=['Rtn-1d'], ascending = False)
            final_dw_df = tkt_dataframe[tkt_dataframe['Rtn-1d'] <= 0.0].sort_values(by=['Rtn-1d'], ascending = True)
            columnVal = 'Rtn-1d'
        if timeRange == '1W':
            final_up_df = tkt_dataframe[tkt_dataframe['Rtn-5d'] > 0.0].sort_values(by=['Rtn-5d'], ascending = False)
            final_dw_df = tkt_dataframe[tkt_dataframe['Rtn-5d'] <= 0.0].sort_values(by=['Rtn-5d'], ascending = True)
            columnVal = 'Rtn-5d'
        if timeRange == '1M':
            final_up_df = tkt_dataframe[tkt_dataframe['Rtn-1mo'] > 0.0].sort_values(by=['Rtn-1mo'], ascending = False)
            final_dw_df = tkt_dataframe[tkt_dataframe['Rtn-1mo'] <= 0.0].sort_values(by=['Rtn-1mo'], ascending = True)
            columnVal = 'Rtn-1mo'
        if timeRange == '1Q':
            final_up_df = tkt_dataframe[tkt_dataframe['Rtn-3mo'] > 0.0].sort_values(by=['Rtn-3mo'], ascending = False)
            final_dw_df = tkt_dataframe[tkt_dataframe['Rtn-3mo'] <= 0.0].sort_values(by=['Rtn-3mo'], ascending = True)
            columnVal = 'Rtn-3mo'
        if timeRange == '1H':
            final_up_df = tkt_dataframe[tkt_dataframe['Rtn-6mo'] > 0.0].sort_values(by=['Rtn-6mo'], ascending = False)
            final_dw_df = tkt_dataframe[tkt_dataframe['Rtn-6mo'] <= 0.0].sort_values(by=['Rtn-6mo'], ascending = True)
            columnVal = 'Rtn-6mo'
        if timeRange == '1Y':
            final_up_df = tkt_dataframe[tkt_dataframe['Rtn-1yr'] > 0.0].sort_values(by=['Rtn-1yr'], ascending = False)
            final_dw_df = tkt_dataframe[tkt_dataframe['Rtn-1yr'] <= 0.0].sort_values(by=['Rtn-1yr'], ascending = True)
            columnVal = 'Rtn-1yr'
        # set output directory and open output file
        os.chdir(outputDir)
        etfFileName = filePrefix + '_etfperf_' + timeRange + '.txt'
        etfFile = open(etfFileName, 'w')
        # Print to the file and also to the console
        tkts_str =''
        etfStartLine = '*** Print ETF UP - ' + timeRange + ' - (' + str(numberToPrintInt) + ') ***'
        print(etfStartLine)
        etfFile.write(etfStartLine + '\n')
        for row in final_up_df.head(numberToPrintInt).iterrows():
            etfLine = row[1]['Symbol'] + '\t' + row[1]['Name'] + '\t' + str(row[1]['Price']) + '\t' + str(row[1][columnVal])
            print(etfLine)
            etfFile.write(etfLine + '\n')
            tkts_str = tkts_str + row[1]['Symbol'] + ','
        etfFinalLine = "tkts_up_str = https://www.finviz.com/screener.ashx?v=351&ft=4&t=" + tkts_str[:(len(tkts_str)-1)] + "&o=-change"
        print(etfFinalLine)
        etfFile.write(etfFinalLine + '\n')

        tkts_str =''
        etfStartLine = '*** Print ETF DOWN - ' + timeRange + ' - (' + str(numberToPrintInt) + ') ***'
        print(etfStartLine)
        etfFile.write(etfStartLine + '\n')        
        for row in final_dw_df.head(numberToPrintInt).iterrows():
            etfLine = row[1]['Symbol'] + '\t' + row[1]['Name'] + '\t' + str(row[1]['Price']) + '\t' + str(row[1][columnVal])
            print(etfLine)
            etfFile.write(etfLine + '\n')
            tkts_str = tkts_str + row[1]['Symbol'] + ','
        etfFinalLine = "tkts_down_str = https://www.finviz.com/screener.ashx?v=351&ft=4&t=" + tkts_str[:(len(tkts_str)-1)] + "&o=-change"
        print(etfFinalLine)
        etfFile.write(etfFinalLine + '\n')
        #close the file
        etfFile.close()
'''
    This  function store in a CSV file values from finviz
    Specifically:
        Overview
        Technical
        Performance
        
    Needs to receive filename prefix, output directory
'''
def etfDailyData(filePrefix, outputDir):
    src = 'screener_results.csv'
    filtro = ['ind_exchangetradedfund']
    tables_list = ['Overview',
                   'Performance',
                   'Technical']
    desc_change = '-change'

    
    os.chdir(outputDir)
    dirpath = os.getcwd()
    print("current directory is : " + dirpath)
    
    for tabla in tables_list:
        stk_list = Screener(filters= filtro, order= desc_change, table= tabla)
        stk_list.to_csv(src)
        dst = filePrefix + '_etf_' + tabla.lower() + '.csv'
        os.rename(src, dst)
    return 0
        
def stkDailyDataO(filePrefix, outputDir):
    src = 'screener_results.csv'
    filtro = ['ind_stocksonly']
    tables_list = ['Overview']
    desc_change = '-change'

    
    os.chdir(outputDir)
    dirpath = os.getcwd()
    print("current directory is : " + dirpath)
    
    for tabla in tables_list:
        print("tabla stkDailyData " + tabla)
        stk_list = Screener(filters= filtro, order= desc_change, table= 'Overview')
        stk_list.to_csv(src)
        dst = filePrefix + '_stk_o_' + tabla.lower() + '.csv'
        os.rename(src, dst)
    return 0  

def stkDailyDataP(filePrefix, outputDir):
    src = 'screener_results.csv'
    filtro = ['ind_stocksonly']
    tables_list = ['Performance']
    desc_change = '-change'

    
    os.chdir(outputDir)
    dirpath = os.getcwd()
    print("current directory is : " + dirpath)
    
    for tabla in tables_list:
        print("tabla stkDailyData " + tabla)
        stk_list = Screener(filters= filtro, order= desc_change, table= tabla)
        stk_list.to_csv(src)
        dst = filePrefix + '_stk_p_' + tabla.lower() + '.csv'
        os.rename(src, dst)
    return 0 

def stkDailyDataT(filePrefix, outputDir):
    src = 'screener_results.csv'
    filtro = ['ind_stocksonly']
    tables_list = ['Technical']
    desc_change = '-change'

    
    os.chdir(outputDir)
    dirpath = os.getcwd()
    print("current directory is : " + dirpath)
    
    for tabla in tables_list:
        print("tabla stkDailyData " + tabla)
        stk_list = Screener(filters= filtro, order= desc_change, table= tabla)
        stk_list.to_csv(src)
        dst = filePrefix + '_stk_t_' + tabla.lower() + '.csv'
        os.rename(src, dst)
    return 0  
    
def spyDailyData(filePrefix, outputDir):
    src = 'screener_results.csv'
    filtro = ['ind_stocksonly', 'idx_sp500']
    tables_list = ['Overview',
                   'Valuation',
                   'Financial',
                   'Ownership',
                   'Performance',
                   'Technical']
    desc_change = '-change'

    
    os.chdir(outputDir)
    dirpath = os.getcwd()
    print("current directory is : " + dirpath)
    
    for tabla in tables_list:
        print("tabla spyDailyData " + tabla)
        stk_list = Screener(filters= filtro, order= desc_change, table= tabla)
        stk_list.to_csv(src)
        dst = filePrefix + '_spy_' + tabla.lower() + '.csv'
        os.rename(src, dst)
        
    return 0

def diaDailyData(filePrefix, outputDir):
    src = 'screener_results.csv'
    filtro = ['ind_stocksonly', 'idx_dji']
    tables_list = ['Overview',
                   'Valuation',
                   'Financial',
                   'Ownership',
                   'Performance',
                   'Technical']
    desc_change = '-change'

    
    os.chdir(outputDir)
    dirpath = os.getcwd()
    print("current directory is : " + dirpath)
    
    for tabla in tables_list:
        print("tabla diaDailyData " + tabla)
        stk_list = Screener(filters= filtro, order= desc_change, table= tabla)
        stk_list.to_csv(src)
        dst = filePrefix + '_dia_' + tabla.lower() + '.csv'
        os.rename(src, dst)
    return 0


'''
    This  function returns a list of etfs extrated from table "Overview"

'''
def etfDailyDataList():
    filtro = ['ind_exchangetradedfund']
    tabla = 'Overview'
    desc_change = '-change'
    
    stk_list = Screener(filters= filtro, order= desc_change, table= tabla)
    etf_price_dict = dict()
    for row in stk_list.data:
        tkt_str = row['Ticker'] 
        tkt_price = row['Price']
        if not tkt_str in  etf_price_dict.keys():
            etf_price_dict[tkt_str] = tkt_price
        else:
            print("this tkt is repeated " + tkt_str)
    print(etf_price_dict)
    return etf_price_dict


'''
    This  function returns "Overview" for Ticket tkt

'''
def TktOverview(tkt):

    print("tabla TktOverview " + tkt)
    stk_list = Screener(tickers= [tkt], table= 'Overview')
    return stk_list


'''
    This  function returns daily "Overview" Table for Sectors Screen

'''
def DailySectorsScreen():
    sectorsTktList = ['IWM','XLF','EEM','XLE','XLK',
                      'XLV','IYT','XLU','XLI','XLY',
                      'IYR','XLP','XLB','TLT','GLD',
                      'UUP','RTH','IYZ','SMH','DBC','USO']
    return Screener(tickers=sectorsTktList, table='Overview', order='-change')

'''
    This  function returns weekly "Performance" Table for Sectors Screen

'''
def WeeklySectorsScreen():
    sectorsTktList = ['IWM','XLF','EEM','XLE','XLK',
                      'XLV','IYT','XLU','XLI','XLY',
                      'IYR','XLP','XLB','TLT','GLD',
                      'UUP','RTH','IYZ','SMH','DBC','USO']
    return Screener(tickers=sectorsTktList, table='Performance', order='-perf1w')

def MonthSectorsScreen():
    sectorsTktList = ['IWM','XLF','EEM','XLE','XLK',
                      'XLV','IYT','XLU','XLI','XLY',
                      'IYR','XLP','XLB','TLT','GLD',
                      'UUP','RTH','IYZ','SMH','DBC','USO']
    return Screener(tickers=sectorsTktList, table='Performance', order='-perf1w')

'''
    This  function returns weekly "Performance" Table for Sectors Screen

'''
def YTDSectorsScreen():
    sectorsTktList = ['IWM','XLF','EEM','XLE','XLK',
                      'XLV','IYT','XLU','XLI','XLY',
                      'IYR','XLP','XLB','TLT','GLD',
                      'UUP','RTH','IYZ','SMH','DBC','USO']
    return Screener(tickers=sectorsTktList, table='Performance', order='-perfytd')

'''
    This function will retun a Screener object with the information requested 
    via the list parameters
'''
def TktScreeenTable(tktList, extractTable, extractOrder):
    return Screener(tickers=tktList, table=extractTable, order=extractOrder)

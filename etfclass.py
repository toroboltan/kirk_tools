'''
Created on Sep 26, 2019

@author: CEVDEA
'''

import finviz
from etfutils import float_or_na, tktTxtLineParser

cons_Rtn1d = '1d'
cons_formatTxt = 'txt'
cons_formatHtml = 'html'
cons_flag_etf_trad = 0
cons_flag_etf_new = 1

class tktEtfScreen():
    """
    Creates a generic message object to store each tkt got from reading etfscreen.txt file
    it basically parses each tab-separated line at puts it into each designated field
    
    Name    Symbol    RSf    Rtn-1d    Rtn-5d    Rtn-1mo    Rtn-3mo    Rtn-6mo    Rtn-1yr    $vol-21
    
    \tSPDR Oil & Gas Eqpmt & Svcs\tXES\t2.29\t6.32\t12.40\t3.20\t-9.18\t-26.23\t-46.49\t10m\n
    """
    
    nameTkt_s = ''
    symbolTkt_s = ''
    priceTkt = 0.0
    rsfTkt_f = 0.0
    rtn1dTkt_f = 0.0
    rtn5dTkt_f = 0.0
    rtn1mTkt_f = 0.0
    rtn3mTkt_f = 0.0
    rtn6mTkt_f = 0.0
    rtn1yTkt_f = 0.0
    vol21Tkt_s = ''
    rawTkt_s = ''

    
    def __init__(self, line, sourceFormat, flag_process, etf_dict):
        self.rawTkt_s = line
        self.tktParser(sourceFormat, flag_process, etf_dict)

        
    def tktParser(self, sourceFormat, flag_process, etf_dict):
        tktParsed_L = tktTxtLineParser(self.rawTkt_s, sourceFormat)
        self.nameTkt_s = tktParsed_L[1]
        self.symbolTkt_s = tktParsed_L[2]
        self.rsfTkt_f = tktParsed_L[3]
        self.rtn1dTkt_f = tktParsed_L[4]
        self.rtn5dTkt_f = tktParsed_L[5]
        self.rtn1mTkt_f = tktParsed_L[6]
        self.rtn3mTkt_f = tktParsed_L[7]
        self.rtn6mTkt_f = tktParsed_L[8]
        self.rtn1yTkt_f = tktParsed_L[9]
        self.vol21Tkt_s = tktParsed_L[10]
        self.priceTkt = self.tktPrice(self.symbolTkt_s, flag_process, etf_dict)
        

    def tktPrintSymbol(self):
        return(self.symbolTkt_s + '\t' + self.nameTkt_s + '\t' +  self.rtn1dTkt_f)
    
    def tktPrintRtn(self, rtnTimeframe_s):
        if(rtnTimeframe_s == cons_Rtn1d):
            return self.rtn1dTkt_f
        else:
            return "Not implemented yet"

    def tktPrice(self, tkt, flag_process, etf_dict):
        if flag_process == cons_flag_etf_trad:
            try:
                price = finviz.get_stock(tkt)['Price']
            except Exception:
                price = 'n/a'
                print("price not found in finviz for: " + tkt)
        elif flag_process == cons_flag_etf_new:
            if tkt in etf_dict.keys():
                price = etf_dict[tkt]
            else:
                price = 'n/a'
        return float_or_na(price)

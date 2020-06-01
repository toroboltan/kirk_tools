'''
Created on Sep 4, 2019

@author: cevdea
'''
import finviz
# Monthly, Candles, Large, No Technical Analysis
stock_list.get_charts(period='m', chart_type='c', size='l', ta=False)

# period='d' > daily
# period='w' > weekly
# period='m' > monthly

# chart_type='c' > candle
# chart_type='l' > lines

# size='m' > small
# size='l' > large

# ta=True > display technical analysis
# ta=False > ignore technical analysis
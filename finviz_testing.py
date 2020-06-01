import os
import finviz
from finviz.screener import Screener

# filters = ['exch_nasd', 'idx_sp500']  # Shows companies in NASDAQ which are in the S&P500
filters = ['idx_sp500']
filters = ['exch_nasd']
filters = ['ind_exchangetradedfund']
#filters = ['idx_sp500']

dirpath = os.getcwd()
print("current directory is : " + dirpath)
foldername = os.path.basename(dirpath)
print("Directory name is : " + foldername)


# Get the first 50 results sorted by price ascending
stk_overview_list = Screener(filters=filters, order='-change', table='Overview')
stk_performance_list = Screener(filters=filters, order='-change', table='Performance')
stk_technical_list = Screener(filters=filters, order='-change', table='Technical')

# Export the screener results to .csv
stk_technical_list.to_csv()

# Create a SQLite database
#stock_list.to_sqlite()



# Add more filters
#stock_list.add(filters=['fa_div_high'])  # Show stocks with high dividend yield
# or just stock_list(filters=['fa_div_high'])

# Print the table into the console
#print(stk_overview_list)

#print(finviz.get_stock('AAPL'))

for stock in stk_overview_list[:5]:  # Loop through 10th - 20th stocks
    print(stock) # Print symbol and price
    
for stock in stk_performance_list[:5]:
    print(stock)

for stock in stk_technical_list[:5]: 
    print(stock)

    

    



#tickers = ['SPY']
#stock_list2 = Screener(tickers=tickers, order='price')
#stock_list2.get_charts(period='m', chart_type='c', size='l', ta=False)

# https://www.finviz.com/chart.ashx?t=SPY&ta=1&ty=c&p=d&s=l

print('end')
import yfinance as yf
import pandas as pd
#define the ticker symbol
tickerSymbol = 'ITC.NS'

#get data on this ticker
tickerData = yf.Ticker(tickerSymbol)

#get the historical prices for this ticker

tickerDf = tickerData.history(period='1d', start='1994-11-03', end='2021-4-16')
df = pd.DataFrame(tickerDf)
df.to_csv(r'C:\Users\Admin\PycharmProjects\Practice\practice code\ITC.csv')
print(tickerDf)

print (df)

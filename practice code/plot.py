import yfinance as yf
import matplotlib.pyplot as plt
import seaborn
itc = yf.Ticker("ITC.NS")
#
# # get stock info
# print(msft.info)
#
# # get historical market data
hist = itc.history(period="1d")
#
#
# # Plot everything by leveraging the very powerful matplotlib package
hist['Close'].plot(figsize=(16, 9))
plt.show()
# #define the ticker symbol
# tickerSymbol = 'ITC.NS'
#
# #get data on this ticker
# tickerData = yf.Ticker(tickerSymbol)
#
# #get the historical prices for this ticker
#
# tickerDf = tickerData.history(period='1d', start='2021-1-1', end='2021-4-16')
# df = pd.DataFrame(tickerDf)
# df.to_csv(r'C:\Users\Admin\PycharmProjects\Practice\practice code\ITC.csv')
# print(tickerDf)
#
# print (df)

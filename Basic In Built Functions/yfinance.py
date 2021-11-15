import yfinance as yf
import pandas as pd
import datetime as dt

asset = "TSLA"
intraday = yf.download(asset, start = "2021-03-17", end = "2021-03-18", interval = "1m")

def Intradaytrend(df, entry, exit):
    ret_120min = df.iloc[120].Open/df.iloc[0].Open -1
    tickret = df.Open.pct_change()
    if ret_120min > entry:
        buyprice = df.iloc[121].Open
        buytime = df.iloc[121].name
        cumulated = (tickret.loc[buytime:] +1).cumprod() -1
        exittime = cumulated[(cumulated < -exit) | (cumulated > exit)].first_valid_index()
        if exittime == None:
            exitprice = df.iloc[-1].Open
        else:
            exitprice = df.iloc[exittime + dt.timedelta(minutes=1)].Open
        profit = exitprice - buyprice
        profitrel = profit/buyprice
        return profitrel
    else:
        return None


Intradaytrend(intraday, 0.01, 0.01)

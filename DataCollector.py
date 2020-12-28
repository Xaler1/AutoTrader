import yfinance as market
from yahoo_fin import stock_info as si

tickers = si.tickers_sp500()

tickers.remove("BF.B")
tickers.remove("BRK.B")

data = market.download(tickers=" ".join(tickers), interval="1m", group_by="ticker", prepost=False, auto_adjust=False, threads=False, start="2020-12-14", end="2020-12-19")

data.to_csv("sp500.csv")


import yfinance as yf
import pandas as pd

def get_live_data(interval="15m"):
    symbol = "XAUUSD=X"  # TradingView/Yahoo compatible symbol for gold spot
    data = yf.download(tickers=symbol, period="1d", interval=interval, progress=False)
    data = data.dropna()
    data.rename(columns=str.lower, inplace=True)
    return data

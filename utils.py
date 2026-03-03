import yfinance as yf
import pandas as pd

def prepare_data(saham):
    df = yf.download(saham + ".JK", period="3mo", progress=False)
    df = df.reset_index()
    df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    df["MA20"] = df["Close"].rolling(20).mean()
    df["MA50"] = df["Close"].rolling(50).mean()
    df = df.dropna()
    return df

import yfinance as yf
import pandas as pd
import numpy as np

features = ["Open", "High", "Low", "Close", "Volume"]

def prepare_data(saham):
    # download data
    df = yf.download(saham + ".JK", period="3mo", progress=False)
    
    # flatten kolom jika multi-index
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ['_'.join([str(c) for c in col if c]).strip() for col in df.columns.values]
    
    df = df.reset_index()
    
    # pilih kolom standar
    col_map = {}
    for col in ["Open", "High", "Low", "Close", "Volume"]:
        # cari kolom yang mengandung kata kunci (case-insensitive)
        found = [c for c in df.columns if col.lower() in c.lower()]
        if not found:
            raise ValueError(f"Kolom {col} tidak ditemukan di df")
        col_map[col] = found[0]  # ambil kolom pertama yang cocok
    
    df = df.rename(columns=col_map)
    
    # hitung MA20 & MA50
    df["MA20"] = df["Close"].rolling(20).mean()
    df["MA50"] = df["Close"].rolling(50).mean()
    
    # drop baris NaN
    df = df.dropna().reset_index(drop=True)
    
    return df

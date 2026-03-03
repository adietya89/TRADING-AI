import yfinance as yf
import pandas as pd
import numpy as np

features = ["Open", "High", "Low", "Close", "Volume"]

def prepare_data(saham):
    df = yf.download(saham + ".JK", period="3mo", progress=False)
    
    # Flatten kolom jika multiindex
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ['_'.join(col).strip() for col in df.columns.values]
    
    df = df.reset_index()
    
    # Pastikan kolom yang kita mau ada
    needed_cols = ["Date", "Open", "High", "Low", "Close", "Volume"]
    for col in needed_cols:
        if col not in df.columns:
            raise ValueError(f"Kolom {col} tidak ditemukan di df")
    
    # Tambah MA20 dan MA50
    df["MA20"] = df["Close"].rolling(20).mean()
    df["MA50"] = df["Close"].rolling(50).mean()
    
    # Hapus baris yang masih NaN (karena MA20/MA50 awal NaN)
    df = df.dropna().reset_index(drop=True)
    
    return df

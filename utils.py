import yfinance as yf
import pandas as pd
import numpy as np

# daftar fitur
features = ["Open", "High", "Low", "Close", "Volume"]

# fungsi ambil data saham
def prepare_data(saham):
    df = yf.download(saham + ".JK", period="3mo", progress=False)
    
    # flatten kolom jika multi-index
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ['_'.join(col).strip() for col in df.columns.values]
    
    df = df.reset_index()
    
    # pastikan kolom yang dibutuhkan ada
    needed_cols = ["Date", "Open", "High", "Low", "Close", "Volume"]
    for col in needed_cols:
        if col not in df.columns:
            raise ValueError(f"Kolom {col} tidak ditemukan di df")
    
    # MA20 & MA50
    df["MA20"] = df["Close"].rolling(20).mean()
    df["MA50"] = df["Close"].rolling(50).mean()
    
    # drop baris NaN
    df = df.dropna().reset_index(drop=True)
    
    return df

# model dummy supaya app jalan
class DummyModel:
    def predict_proba(self, X):
        return [[0.3, 0.7]]

model_xgb = DummyModel()
model_lstm = DummyModel()

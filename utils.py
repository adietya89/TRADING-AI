import yfinance as yf
import pandas as pd
import numpy as np

# fitur yang digunakan
features = ["Open", "High", "Low", "Close", "Volume"]

def prepare_data(saham):
    # Ambil data 3 bulan terakhir
    df = yf.download(saham + ".JK", period="3mo", progress=False)

    # flatten kolom jika multi-index
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ['_'.join([str(c) for c in col if c]).strip() for col in df.columns.values]

    df = df.reset_index()

    # map kolom ke standar
    col_map = {}
    for col in ["Open", "High", "Low", "Close", "Volume"]:
        found = [c for c in df.columns if col.lower() in c.lower()]
        if not found:
            raise ValueError(f"Kolom {col} tidak ditemukan di df")
        col_map[col] = found[0]
    df = df.rename(columns=col_map)

    # Tambah MA20 & MA50
    df["MA20"] = df["Close"].rolling(20).mean()
    df["MA50"] = df["Close"].rolling(50).mean()

    # Drop NaN
    df = df.dropna().reset_index(drop=True)

    return df

# model dummy untuk prediksi probabilitas naik
class DummyModel:
    def predict_proba(self, X):
        return [[0.3, 0.7]]

model_xgb = DummyModel()
model_lstm = DummyModel()

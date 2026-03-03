import yfinance as yf
import pandas as pd
import numpy as np
from xgboost import XGBClassifier
import joblib
import os

features = ["Open", "High", "Low", "Close", "Volume"]
MODEL_FILE = "xgb_model.pkl"

def prepare_data(saham):
    df = yf.download(saham + ".JK", period="3mo", progress=False)

    if df.empty:
        raise ValueError(f"Data saham {saham} tidak tersedia")

    # flatten MultiIndex jika ada
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ['_'.join([str(c) for c in col if c]).strip() for col in df.columns.values]

    df = df.reset_index()

    # map kolom ke standar
    col_map = {}
    for col in features:
        found = [c for c in df.columns if col.lower() in c.lower()]
        if not found:
            raise ValueError(f"Kolom {col} tidak ditemukan. Kolom tersedia: {df.columns.tolist()}")
        col_map[col] = found[0]
    df = df.rename(columns=col_map)

    # hitung MA20 & MA50
    df["MA20"] = df["Close"].rolling(20).mean()
    df["MA50"] = df["Close"].rolling(50).mean()

    # drop NaN
    df = df.dropna().reset_index(drop=True)
    return df

def load_xgb_model():
    if os.path.exists(MODEL_FILE):
        model = joblib.load(MODEL_FILE)
    else:
        # buat model dummy jika file tidak ada
        model = XGBClassifier()
        model.fit(np.random.rand(50, len(features)), np.random.randint(0,2,50))
        joblib.dump(model, MODEL_FILE)
    return model

model_xgb = load_xgb_model()

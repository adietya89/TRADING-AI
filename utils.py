import yfinance as yf
import pandas as pd
import numpy as np

features = ["Open", "High", "Low", "Close", "Volume"]

def prepare_data(saham):
    df = yf.download(saham + ".JK", period="3mo", progress=False)
    
    # Jika multi-level columns, ratakan jadi satu level dengan join '_'
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ['_'.join(col).strip() for col in df.columns.values]
    
    df = df.reset_index()
    df["MA20"] = df["Close"].rolling(20).mean()
    df["MA50"] = df["Close"].rolling(50).mean()
    df = df.dropna()
    return df

class DummyModel:
    def predict_proba(self, X):
        # Prediksi dummy: 70% peluang naik
        return [[0.3, 0.7]]

model_xgb = DummyModel()
model_lstm = DummyModel()

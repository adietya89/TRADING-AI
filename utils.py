import yfinance as yf
import pandas as pd
import numpy as np
from xgboost import XGBClassifier

features = ["Close", "MA20", "MA50"]

def prepare_data(saham):
    try:
        df = yf.download(saham + ".JK", period="3mo", progress=False)
        df = df.reset_index()
        df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]

        df["MA20"] = df["Close"].rolling(20).mean()
        df["MA50"] = df["Close"].rolling(50).mean()
        df = df.dropna()
        return df
    except Exception as e:
        print(f"Error ambil data {saham}: {e}")
        return None

# Dummy XGB model
def load_xgb_model():
    model = XGBClassifier()
    model.predict_proba = lambda X: np.array([[0.3, 0.7]])  # dummy 70% naik
    return model

model_xgb = load_xgb_model()

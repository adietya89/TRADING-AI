import yfinance as yf
import pandas as pd
import numpy as np
from xgboost import XGBClassifier

features = ["Close", "MA20", "MA50"]

def prepare_data(saham):
    try:
        df = yf.download(saham + ".JK", period="6mo", progress=False)
        df = df.reset_index()
        df = df[['Date','Open','High','Low','Close','Volume']]

        # MA20 & MA50
        df['MA20'] = df['Close'].rolling(20).mean()
        df['MA50'] = df['Close'].rolling(50).mean()

        # RSI 14
        delta = df['Close'].diff()
        up = delta.clip(lower=0)
        down = -1*delta.clip(upper=0)
        roll_up = up.rolling(14).mean()
        roll_down = down.rolling(14).mean()
        rs = roll_up / roll_down
        df['RSI'] = 100 - (100 / (1+rs))

        # MACD
        df['EMA12'] = df['Close'].ewm(span=12, adjust=False).mean()
        df['EMA26'] = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = df['EMA12'] - df['EMA26']
        df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

        df = df.dropna()
        return df
    except Exception as e:
        print(f"Error ambil data {saham}: {e}")
        return None

# Dummy XGB model
def load_xgb_model():
    model = XGBClassifier()
    model.predict_proba = lambda X: np.array([[0.3,0.7]])  # dummy 70% naik
    return model

model_xgb = load_xgb_model()

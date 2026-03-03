import pandas as pd
import numpy as np

# Contoh daftar fitur
features = ["Open", "High", "Low", "Close", "Volume"]

# Fungsi untuk menyiapkan data
def prepare_data(df):
    df = df.copy()
    df = df.dropna()
    return df

# Model XGBoost (dummy dulu supaya tidak error)
def model_xgb(X_train, y_train):
    return "Model XGB berhasil dijalankan (dummy)"

# Model LSTM (dummy dulu supaya tidak error)
def model_lstm(X_train, y_train):
    return "Model LSTM berhasil dijalankan (dummy)"

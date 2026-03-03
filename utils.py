import yfinance as yf
import pandas as pd
import numpy as np

features = ["Open", "High", "Low", "Close", "Volume"]

def prepare_data(saham):
    df = yf.download(saham + ".JK", period="3mo", progress=False)

    # Jika data kosong, buat dummy supaya app tetap jalan
    if df.empty:
        dates = pd.date_range(end=pd.Timestamp.today(), periods=60)
        df = pd.DataFrame({
            "Date": dates,
            "Open": np.random.rand(60)*1000,
            "High": np.random.rand(60)*1000,
            "Low": np.random.rand(60)*1000,
            "Close": np.random.rand(60)*1000,
            "Volume": np.random.randint(1000,10000, size=60)
        })

    # Flatten MultiIndex jika ada
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ['_'.join([str(c) for c in col if c]).strip() for col in df.columns.values]

    df = df.reset_index()

    # Cari kolom Close yang tersedia
    close_col = None
    for c in df.columns:
        if "close" in c.lower():
            close_col = c
            break
    if close_col is None:
        raise ValueError(f"Tidak ada kolom Close di data. Kolom tersedia: {df.columns.tolist()}")
    df = df.rename(columns={close_col: "Close"})

    # Rename kolom lain yang ada
    for col in ["Open","High","Low","Volume"]:
        for c in df.columns:
            if col.lower() in c.lower():
                df = df.rename(columns={c: col})
                break

    # Tambah MA20 & MA50
    df["MA20"] = df["Close"].rolling(20).mean()
    df["MA50"] = df["Close"].rolling(50).mean()
    df = df.dropna().reset_index(drop=True)
    return df

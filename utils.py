import pandas as pd
import numpy as np

features = ["Open", "High", "Low", "Close", "Volume"]

def prepare_data(saham):
    # bikin data dummy supaya tidak error
    dates = pd.date_range(end=pd.Timestamp.today(), periods=100)
    
    df = pd.DataFrame({
        "Date": dates,
        "Open": np.random.rand(100)*100,
        "High": np.random.rand(100)*100,
        "Low": np.random.rand(100)*100,
        "Close": np.random.rand(100)*100,
        "Volume": np.random.randint(1000, 5000, 100)
    })
    
    df["MA20"] = df["Close"].rolling(20).mean()
    df["MA50"] = df["Close"].rolling(50).mean()
    
    return df

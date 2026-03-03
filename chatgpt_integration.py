import pandas as pd
import numpy as np

def analyze_stock(df, saham):
    close = df['Close'].iloc[-1]
    ma20 = df['MA20'].iloc[-1]
    ma50 = df['MA50'].iloc[-1]

    # Trend
    trend = "bullish" if ma20 > ma50 else "bearish / sideways"

    # Support & Resistance sederhana
    support = df['Close'].min()
    resistance = df['Close'].max()

    # RSI sederhana
    delta = df['Close'].diff()
    up = delta.clip(lower=0)
    down = -1*delta.clip(upper=0)
    roll_up = up.rolling(14).mean()
    roll_down = down.rolling(14).mean()
    rs = roll_up / roll_down
    rsi = 100 - (100 / (1 + rs))
    rsi_last = rsi.iloc[-1]

    # Output AI Lokal
    text = f"""
📈 Analisis Saham {saham} (AI Lokal)
Harga terakhir: Rp {close:,.0f}
Trend: {trend}
MA20: {ma20:,.0f}, MA50: {ma50:,.0f}
Support: Rp {support:,.0f}, Resistance: Rp {resistance:,.0f}
RSI: {rsi_last:.2f} → {'Overbought' if rsi_last>70 else 'Oversold' if rsi_last<30 else 'Netral'}

Skenario Pergerakan:
- Jika harga menembus resistance → potensi bullish
- Jika harga turun di bawah support → potensi koreksi

Strategi Umum:
- Trader Harian: Entry dekat support, TP dekat resistance
- Swing Trader: Tunggu breakout jelas sebelum akumulasi

⚠️ Catatan: Ini analisis lokal, bukan rekomendasi beli/jual.
"""
    return text

def ask_ai(saham, df, question=None, mode="local"):
    return analyze_stock(df, saham)

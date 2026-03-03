# chatgpt_integration.py
import numpy as np

def analyze_stock(df, saham, question=None):
    # Ambil row terakhir
    try:
        last_row = df.iloc[-1]
    except IndexError:
        return f"Data untuk saham {saham} tidak tersedia."

    # Ambil data penting dengan pengecekan
    def safe_get(key):
        val = last_row.get(key, None)
        if val is None or not isinstance(val, (int, float)) or np.isnan(val):
            return "N/A"
        return val

    close = safe_get('Close')
    ma20 = safe_get('MA20')
    ma50 = safe_get('MA50')
    rsi = safe_get('RSI')
    macd = safe_get('MACD')
    signal = safe_get('Signal')

    # Support & Resistance
    support = df['Close'].min() if 'Close' in df.columns and not df['Close'].empty else "N/A"
    resistance = df['Close'].max() if 'Close' in df.columns and not df['Close'].empty else "N/A"

    # Trend
    trend = "bullish" if isinstance(ma20, (int,float)) and isinstance(ma50, (int,float)) and ma20 > ma50 else "bearish / sideways"
    macd_trend = "Buy" if isinstance(macd, (int,float)) and isinstance(signal, (int,float)) and macd > signal else "Sell / Sideways"
    rsi_status = "Overbought" if isinstance(rsi, (int,float)) and rsi > 70 else "Oversold" if isinstance(rsi, (int,float)) and rsi < 30 else "Netral"

    # Format angka jika valid
    def fmt(val):
        if isinstance(val, (int,float)):
            return f"{val:,.0f}" if val == int(val) else f"{val:,.2f}"
        return val

    text = f"""
📈 Analisis Saham {saham} (AI Lokal)

Trend MA: {trend}
MA20: {fmt(ma20)}, MA50: {fmt(ma50)}
RSI: {fmt(rsi)} → {rsi_status}
MACD: {fmt(macd)} ({macd_trend})
Support: Rp {fmt(support)}, Resistance: Rp {fmt(resistance)}
Harga Terakhir: Rp {fmt(close)}

Skenario Pergerakan:
- Jika harga menembus resistance → potensi bullish
- Jika harga turun di bawah support → potensi koreksi

Strategi:
- Trader Harian: Entry dekat support, TP dekat resistance
- Swing Trader: Tunggu breakout jelas sebelum akumulasi

Pertanyaanmu: {question if question else "Tidak ada pertanyaan spesifik"}

⚠️ Catatan: Analisis lokal, bukan rekomendasi beli/jual.
"""
    return text

def ask_ai(saham, df, question=None, mode="local"):
    return analyze_stock(df, saham, question)

import numpy as np

def calculate_rsi(df, period=14):
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def ask_ai(saham, df, question):

    close_price = df["Close"].iloc[-1]
    ma20 = df["MA20"].iloc[-1]
    ma50 = df["MA50"].iloc[-1]

    # Hitung RSI
    df["RSI"] = calculate_rsi(df)
    rsi = df["RSI"].iloc[-1]

    # Support & Resistance sederhana
    support = df["Low"].rolling(20).min().iloc[-1]
    resistance = df["High"].rolling(20).max().iloc[-1]

    # Trend logic
    if ma20 > ma50:
        trend = "cenderung bullish (rebound jangka pendek)"
        bias = "potensi naik lebih besar"
    elif ma20 < ma50:
        trend = "cenderung bearish ringan / sideways"
        bias = "tekanan turun masih ada"
    else:
        trend = "sideways"
        bias = "netral"

    # RSI logic
    if rsi > 70:
        rsi_text = "overbought (jenuh beli)"
    elif rsi < 30:
        rsi_text = "oversold (jenuh jual)"
    else:
        rsi_text = "netral"

    analysis = f"""
📈 1) Trend Harga & Struktur Grafik

Harga terakhir {saham}: Rp {close_price:,.0f}
Pergerakan saat ini {trend}.
Support terdekat di sekitar Rp {support:,.0f}
Resistance terdekat di sekitar Rp {resistance:,.0f}

📊 2) Indikator Teknis

🔹 RSI: {rsi:.2f} → {rsi_text}

🔹 Moving Average:
MA20: {ma20:,.0f}
MA50: {ma50:,.0f}
Struktur MA menunjukkan {bias}.

🕯️ 3) Skenario Pergerakan

Jika harga menembus resistance Rp {resistance:,.0f} dengan volume kuat → potensi breakout naik.

Jika harga turun di bawah support Rp {support:,.0f} → risiko koreksi lanjutan.

💡 4) Strategi Umum

🟢 Trader harian:
Entry dekat support.
Take profit dekat resistance.
Stop loss di bawah support.

🟡 Swing trader:
Tunggu breakout jelas sebelum akumulasi besar.

📌 Kesimpulan

Saham {saham} saat ini dalam kondisi {trend}.
Momentum teknikal menunjukkan {bias}.
RSI berada pada kondisi {rsi_text}.

⚠️ Ini bukan rekomendasi investasi, hanya analisa teknikal berbasis data harga.
"""

    return analysis

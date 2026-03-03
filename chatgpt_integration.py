def analyze_stock(df, saham, question=None):
    close = df['Close'].iloc[-1]
    ma20 = df['MA20'].iloc[-1]
    ma50 = df['MA50'].iloc[-1]
    rsi = df['RSI'].iloc[-1]
    macd = df['MACD'].iloc[-1]
    signal = df['Signal'].iloc[-1]
    support = df['Close'].min()
    resistance = df['Close'].max()

    trend = "bullish" if ma20 > ma50 else "bearish / sideways"
    macd_trend = "Buy" if macd > signal else "Sell / Sideways"
    rsi_status = "Overbought" if rsi>70 else "Oversold" if rsi<30 else "Netral"

    text = f"""
📈 Analisis Saham {saham} (AI Lokal)
def analyze_stock(df, saham, question):
    last_row = df.iloc[-1]
    close = last_row.get('Close', None)

    # cek apakah close valid
    if close is None or not isinstance(close, (int, float)) or np.isnan(close):
        formatted_close = "N/A"
    else:
        formatted_close = f"{close:,.0f}"

    # Contoh jawaban AI
    result = f"Harga terakhir: Rp {formatted_close}\n"
    result += "Analisis lain bisa ditambahkan di sini..."
    return result
Trend MA: {trend}
MA20: {ma20:,.0f}, MA50: {ma50:,.0f}
RSI: {rsi:.2f} → {rsi_status}
MACD: {macd:.2f} ({macd_trend})
Support: Rp {support:,.0f}, Resistance: Rp {resistance:,.0f}

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

from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_ai(saham, df, question):
    try:
        close_price = df["Close"].iloc[-1]
        ma20 = df["MA20"].iloc[-1]
        ma50 = df["MA50"].iloc[-1]

        prompt = f"""
Anda adalah analis teknikal profesional pasar saham Indonesia.

Data terakhir saham {saham}:
Harga terakhir: {close_price}
MA20: {ma20}
MA50: {ma50}

Buat analisa teknikal terstruktur seperti berikut:

1) Trend Harga & Struktur Grafik
2) Indikator Teknis (RSI, MACD, Moving Average)
3) Pola Candlestick
4) Strategi Trader Harian & Swing
5) Kesimpulan

Gunakan bahasa Indonesia profesional.
Pertanyaan tambahan dari user: {question}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"AI tidak dapat menjawab saat ini: {str(e)}"

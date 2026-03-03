from openai import OpenAI
import os
import numpy as np

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def local_analysis(saham, df):
    close_price = df["Close"].iloc[-1]
    ma20 = df["MA20"].iloc[-1]
    ma50 = df["MA50"].iloc[-1]

    trend = "bullish" if ma20 > ma50 else "bearish / sideways"

    return f"""
Analisa Lokal:
Harga terakhir {saham}: {close_price:,.0f}
Trend saat ini: {trend}
MA20: {ma20:,.0f}
MA50: {ma50:,.0f}
"""

def ask_ai(saham, df, question, mode="local"):

    if mode == "local":
        return local_analysis(saham, df)

    if mode == "gpt":
        try:
            close_price = df["Close"].iloc[-1]
            ma20 = df["MA20"].iloc[-1]
            ma50 = df["MA50"].iloc[-1]

            prompt = f"""
Anda adalah analis saham profesional.

Data saham {saham}:
Harga terakhir: {close_price}
MA20: {ma20}
MA50: {ma50}

Buat analisa teknikal lengkap dan terstruktur.
Pertanyaan user: {question}
"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.6
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"AI GPT gagal, fallback ke lokal.\n\n{local_analysis(saham, df)}"

def ask_ai(saham, df, question):
    # Contoh jawaban simpel, nanti bisa sambung ke OpenAI API
    close_price = df['Close'].iloc[-1]
    return f"Analisa untuk {saham}: Harga terakhir adalah {close_price:.2f}. Pertanyaanmu: {question}"

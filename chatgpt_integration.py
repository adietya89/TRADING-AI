def ask_ai(saham, df, question):
    close_price = df['Close'].iloc[-1]
    return f"Analisa (dummy) untuk {saham}: Harga terakhir {close_price:.2f}. Pertanyaanmu: {question}"

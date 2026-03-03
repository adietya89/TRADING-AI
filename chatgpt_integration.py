def ask_ai(saham, df, question):
    return f"Analisa sederhana untuk {saham}: Saat ini harga terakhir adalah {df['Close'].iloc[-1]}"

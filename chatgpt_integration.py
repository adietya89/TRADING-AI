import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_ai(saham, df, question):
    close_price = df['Close'].iloc[-1]
    prompt = f"Harga terakhir {saham} adalah {close_price:.2f}. Pertanyaan: {question} Jawab singkat dalam bahasa Indonesia."

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # Ganti dari gpt-4 ke gpt-3.5-turbo
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI tidak dapat menjawab saat ini: {str(e)}"

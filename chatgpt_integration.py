import openai
import os

# Ambil API key dari environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_ai(saham, df, question):
    close_price = df['Close'].iloc[-1]
    prompt = f"Harga terakhir {saham} adalah {close_price:.2f}. Pertanyaan: {question} Jawab dengan bahasa Indonesia secara singkat dan jelas."
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI tidak dapat menjawab saat ini: {str(e)}"

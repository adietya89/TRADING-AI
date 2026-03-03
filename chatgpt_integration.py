import openai
import os

# Pastikan environment variable OPENAI_API_KEY sudah di-set
openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_ai(saham, df, question):
    close_price = df['Close'].iloc[-1]
    prompt = f"Harga terakhir {saham} adalah {close_price:.2f}. Pertanyaan: {question} Jawab dengan bahasa Indonesia secara singkat dan jelas."
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )
    return response.choices[0].message.content

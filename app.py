import streamlit as st
import plotly.express as px
from utils import prepare_data, model_xgb, features
st.write("Fungsi ask_ai ada?", callable(ask_ai))
from chatgpt_integration import ask_ai

st.title("📈 AI Trading Hedge Fund Dashboard")

saham_list = ["BBRI", "BBCA", "BMRI", "TLKM", "ASII", "ADRO", "ANTM"]
selected_saham = st.selectbox("Pilih Saham", saham_list)

def prepare_data(saham):
    df = yf.download(saham + ".JK", period="3mo", progress=False)
    df = df.reset_index()
    
    # Ambil kolom yang diperlukan dan rename ke nama standar
    df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    
    df["MA20"] = df["Close"].rolling(20).mean()
    df["MA50"] = df["Close"].rolling(50).mean()
    df = df.dropna()
    return df

question = st.text_input("Tanyakan sesuatu tentang saham ini:")
if question:
    answer = ask_ai(selected_saham, df, question)
    st.write(answer)

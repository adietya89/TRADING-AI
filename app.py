import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from utils import prepare_data, model_xgb, features
from chatgpt_integration import ask_ai

st.set_page_config(layout="wide")
st.title("📈 AI Trading Hedge Fund Dashboard")

# Pilih saham
saham_list = ["BBRI","BBCA","BMRI","TLKM","ASII","ADRO","ANTM"]
selected_saham = st.selectbox("Pilih Saham", saham_list)

# Ambil data
df = prepare_data(selected_saham)
if df is None or df.empty:
    st.error("Data tidak tersedia.")
    st.stop()

# Grafik Close + MA20 + MA50 + Support/Resistance
fig = go.Figure()
fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], name="Close", line=dict(color='blue')))
if 'MA20' in df.columns:
    fig.add_trace(go.Scatter(x=df['Date'], y=df['MA20'], name="MA20", line=dict(color='orange')))
if 'MA50' in df.columns:
    fig.add_trace(go.Scatter(x=df['Date'], y=df['MA50'], name="MA50", line=dict(color='purple')))

# Support & Resistance aman
support = df['Close'].min()
resistance = df['Close'].max()
if not pd.isna(support):
    fig.add_hline(y=support, line_dash="dot", line_color="green", annotation_text="Support")
if not pd.isna(resistance):
    fig.add_hline(y=resistance, line_dash="dot", line_color="red", annotation_text="Resistance")

st.plotly_chart(fig, use_container_width=True)

# Prediksi probabilitas naik
last = df[features].tail(1)
proba = model_xgb.predict_proba(last)[0][1]
st.metric("Probabilitas Naik (%)", round(proba*100,2))

# Pilih mode AI
ai_mode = st.radio("Mode AI:", ["Local AI"])  # bisa ditambah ChatGPT kalau API siap

# Input pertanyaan user
question = st.text_input("Tanyakan sesuatu tentang saham ini:")

if question:
    mode = "local" if ai_mode == "Local AI" else "gpt"
    answer = ask_ai(selected_saham, df, question, mode)
    st.markdown(answer)

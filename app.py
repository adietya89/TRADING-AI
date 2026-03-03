import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from utils import prepare_data, model_xgb, features
from chatgpt_integration import ask_ai

st.set_page_config(layout="wide")
st.title("📈 AI Trading Hedge Fund Dashboard")

# --- Pilih Saham ---
saham_list = ["BBRI","BBCA","BMRI","TLKM","ASII","ADRO","ANTM"]
selected_saham = st.selectbox("Pilih Saham", saham_list)

# --- Ambil Data ---
df = prepare_data(selected_saham)
if df is None or df.empty:
    st.error("Data tidak tersedia.")
    st.stop()

# --- Hitung RSI ---
def compute_RSI(data, period=14):
    delta = data.diff()
    gain = delta.clip(lower=0)
    loss = -1*delta.clip(upper=0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

df['RSI'] = compute_RSI(df['Close'])

# --- Hitung MACD ---
def compute_MACD(data, fast=12, slow=26, signal=9):
    ema_fast = data.ewm(span=fast, adjust=False).mean()
    ema_slow = data.ewm(span=slow, adjust=False).mean()
    macd = ema_fast - ema_slow
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    return macd, signal_line

df['MACD'], df['MACD_signal'] = compute_MACD(df['Close'])

# --- Grafik Harga + MA ---
fig = go.Figure()
fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], name="Close", line=dict(color='blue')))
if 'MA20' in df.columns:
    fig.add_trace(go.Scatter(x=df['Date'], y=df['MA20'], name="MA20", line=dict(color='orange')))
if 'MA50' in df.columns:
    fig.add_trace(go.Scatter(x=df['Date'], y=df['MA50'], name="MA50", line=dict(color='purple')))

# --- Support & Resistance ---
support = df['Close'].min()
resistance = df['Close'].max()
try:
    support = float(support)
except:
    support = None
try:
    resistance = float(resistance)
except:
    resistance = None
if support is not None:
    fig.add_hline(y=support, line_dash="dot", line_color="green", annotation_text="Support")
if resistance is not None:
    fig.add_hline(y=resistance, line_dash="dot", line_color="red", annotation_text="Resistance")

st.plotly_chart(fig, use_container_width=True)

# --- Grafik RSI ---
fig_rsi = go.Figure()
fig_rsi.add_trace(go.Scatter(x=df['Date'], y=df['RSI'], name="RSI", line=dict(color='magenta')))
fig_rsi.add_hline(y=70, line_dash="dot", line_color="red", annotation_text="Overbought")
fig_rsi.add_hline(y=30, line_dash="dot", line_color="green", annotation_text="Oversold")
st.plotly_chart(fig_rsi, use_container_width=True)

# --- Grafik MACD ---
fig_macd = go.Figure()
fig_macd.add_trace(go.Scatter(x=df['Date'], y=df['MACD'], name="MACD", line=dict(color='blue')))
fig_macd.add_trace(go.Scatter(x=df['Date'], y=df['MACD_signal'], name="Signal", line=dict(color='orange')))
st.plotly_chart(fig_macd, use_container_width=True)

# --- Prediksi Probabilitas Naik ---
last = df[features].tail(1)
proba = model_xgb.predict_proba(last)[0][1]
st.metric("Probabilitas Naik (%)", round(proba*100,2))

# --- Mode AI ---
ai_mode = st.radio("Mode AI:", ["Local AI", "ChatGPT"])

# --- Input pertanyaan ---
question = st.text_input("Tanyakan sesuatu tentang saham ini:")
if question:
    mode = "local" if ai_mode == "Local AI" else "gpt"
    answer = ask_ai(selected_saham, df, question, mode)
    st.markdown(answer)

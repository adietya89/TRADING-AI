import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from utils import prepare_data, model_xgb, features
from chatgpt_integration import ask_ai

st.set_page_config(layout="wide", page_title="AI Trading Dashboard")
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

# --- Prediksi Probabilitas Naik ---
last = df[features].tail(1)
proba = model_xgb.predict_proba(last)[0][1]
st.metric("Probabilitas Naik (%)", round(proba*100,2))

# --- Pilih Mode AI ---
ai_mode = st.radio("Mode AI:", ["Local AI", "ChatGPT"])
question = st.text_input("Tanyakan sesuatu tentang saham ini:")

# --- Dashboard Tabs ---
tab1, tab2, tab3 = st.tabs(["📊 Harga & MA", "📈 RSI", "📉 MACD"])

# --- Tab Harga & MA ---
with tab1:
    fig_price = go.Figure()
    # Candlestick
    fig_price.add_trace(go.Candlestick(
        x=df['Date'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name="Candlestick"
    ))
    # Moving Averages
    if 'MA20' in df.columns:
        fig_price.add_trace(go.Scatter(x=df['Date'], y=df['MA20'], name="MA20",
                                       line=dict(color='orange', width=2, dash='dash')))
    if 'MA50' in df.columns:
        fig_price.add_trace(go.Scatter(x=df['Date'], y=df['MA50'], name="MA50",
                                       line=dict(color='purple', width=2, dash='dot')))
    
    # Support & Resistance aman
    # --- Support & Resistance aman ---
    if 'Close' in df.columns and not df['Close'].empty:
        support_val = df['Close'].min()
        resistance_val = df['Close'].max()

         # Pastikan scalar & bukan NaN
        if support_val is not None and not pd.isna(support_val):
           fig_price.add_hline(y=float(support_val), line_dash="dot",
                            line_color="green", annotation_text="Support")
        if resistance_val is not None and not pd.isna(resistance_val):
           fig_price.add_hline(y=float(resistance_val), line_dash="dot",
                            line_color="red", annotation_text="Resistance")
    
    fig_price.update_layout(title=f"{selected_saham} Harga & MA",
                            xaxis_title="Tanggal", yaxis_title="Harga",
                            legend_title="Indikator", font=dict(size=14),
                            margin=dict(l=40, r=40, t=40, b=40))
    st.plotly_chart(fig_price, use_container_width=True)

# --- Tab RSI ---
with tab2:
    fig_rsi = go.Figure()
    fig_rsi.add_trace(go.Scatter(x=df['Date'], y=df['RSI'], name="RSI", line=dict(color='magenta', width=2)))
    fig_rsi.add_hline(y=70, line_dash="dot", line_color="red", annotation_text="Overbought")
    fig_rsi.add_hline(y=30, line_dash="dot", line_color="green", annotation_text="Oversold")
    fig_rsi.update_layout(title=f"{selected_saham} RSI", xaxis_title="Tanggal", yaxis_title="RSI")
    st.plotly_chart(fig_rsi, use_container_width=True)

# --- Tab MACD ---
with tab3:
    fig_macd = go.Figure()
    fig_macd.add_trace(go.Scatter(x=df['Date'], y=df['MACD'], name="MACD", line=dict(color='blue', width=2)))
    fig_macd.add_trace(go.Scatter(x=df['Date'], y=df['MACD_signal'], name="Signal", line=dict(color='orange', width=2)))
    fig_macd.update_layout(title=f"{selected_saham} MACD", xaxis_title="Tanggal", yaxis_title="MACD")
    st.plotly_chart(fig_macd, use_container_width=True)

# --- AI Analysis ---
if question:
    mode = "local" if ai_mode == "Local AI" else "gpt"
    answer = ask_ai(selected_saham, df, question, mode)
    st.markdown(answer)

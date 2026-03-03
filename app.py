import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
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

# Grafik Close + MA20 + MA50 + Support/Resistance + RSI + MACD
fig = go.Figure()
fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], name="Close"))
if 'MA20' in df.columns:
    fig.add_trace(go.Scatter(x=df['Date'], y=df['MA20'], name="MA20"))
if 'MA50' in df.columns:
    fig.add_trace(go.Scatter(x=df['Date'], y=df['MA50'], name="MA50"))
support = df['Close'].min()
resistance = df['Close'].max()
fig.add_hline(y=support, line_dash="dot", line_color="green", annotation_text="Support")
fig.add_hline(y=resistance, line_dash="dot", line_color="red", annotation_text="Resistance")
st.plotly_chart(fig, use_container_width=True)

# Probabilitas Naik
last = df[features].tail(1)
proba = model_xgb.predict_proba(last)[0][1]
st.metric("Probabilitas Naik (%)", round(proba*100,2))

# AI Lokal
st.subheader("🤖 AI Analisis Saham")
question = st.text_input("Tanyakan sesuatu tentang saham ini:")
if question:
    answer = ask_ai(selected_saham, df, question)
    st.write(answer)

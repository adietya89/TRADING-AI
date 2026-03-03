import streamlit as st
from utils import prepare_data, model_xgb, model_lstm, features
from chatgpt_integration import ask_ai
import plotly.express as px

st.title("📈 AI Trading Hedge Fund Dashboard")

saham_list = ["BBRI","BBCA","BMRI","TLKM","ASII","ADRO","ANTM"]
selected_saham = st.selectbox("Pilih Saham", saham_list)

df = prepare_data(selected_saham)
last = df[features].tail(1)
proba = model_xgb.predict_proba(last)[0][1]
st.metric("Probabilitas Naik (%)", round(proba*100,2))

fig = px.line(df, y=['Close','MA20','MA50'], title=f"{selected_saham} Chart")
st.plotly_chart(fig)

question = st.text_input("Tanyakan sesuatu tentang saham ini:")
if question:
    answer = ask_ai(selected_saham, df, question)
    st.write(answer)


import streamlit as st
import plotly.express as px
from utils import prepare_data, model_xgb, features
from chatgpt_integration import ask_ai

st.title("📈 AI Trading Hedge Fund Dashboard")

# Pilihan saham
saham_list = ["BBRI", "BBCA", "BMRI", "TLKM", "ASII", "ADRO", "ANTM"]
selected_saham = st.selectbox("Pilih Saham", saham_list)

# Ambil data
df = prepare_data(selected_saham)

# Plot grafik Close + MA20 + MA50
df_long = df.melt(id_vars=["Date"], value_vars=["Close", "MA20", "MA50"],
                  var_name="Indicator", value_name="Value")
fig = px.line(df_long, x="Date", y="Value", color="Indicator",
              title=f"{selected_saham} Chart")
st.plotly_chart(fig)

# Prediksi probabilitas naik
last = df[features].tail(1)
proba = model_xgb.predict_proba(last)[0][1]
st.metric("Probabilitas Naik (%)", round(proba*100,2))

# Input pertanyaan user
question = st.text_input("Tanyakan sesuatu tentang saham ini:")
if question:
    answer = ask_ai(selected_saham, df, question)
    st.write(answer)

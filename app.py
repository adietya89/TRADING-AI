import streamlit as st
import plotly.express as px
from utils import prepare_data, model_xgb, features
from chatgpt_integration import ask_ai

st.title("📈 AI Trading Hedge Fund Dashboard")

# Pilih saham
saham_list = ["BBRI", "BBCA", "BMRI", "TLKM", "ASII", "ADRO", "ANTM"]
selected_saham = st.selectbox("Pilih Saham", saham_list)

# Ambil data
df = prepare_data(selected_saham)
if df is None or df.empty:
    st.error("Data tidak tersedia.")
    st.stop()

# Grafik Close + MA20 + MA50 + Support/Resistance
support = df['Close'].min()
resistance = df['Close'].max()
df_long = df.melt(id_vars=["Date"], value_vars=["Close", "MA20", "MA50"],
                  var_name="Indicator", value_name="Value")
fig = px.line(df_long, x="Date", y="Value", color="Indicator",
              title=f"{selected_saham} Chart")
# Tambah garis support & resistance
fig.add_hline(y=support, line_dash="dot", line_color="green", annotation_text="Support")
fig.add_hline(y=resistance, line_dash="dot", line_color="red", annotation_text="Resistance")
st.plotly_chart(fig)

# Prediksi probabilitas naik (dummy)
last = df[features].tail(1)
proba = model_xgb.predict_proba(last)[0][1]
st.metric("Probabilitas Naik (%)", round(proba*100,2))

# =============================
# 🔥 AI Lokal
# =============================
st.subheader("🤖 AI Analysis")

# Pilih mode AI (hanya lokal)
ai_mode = st.radio("Mode AI:", ["Local AI"])

question = st.text_input("Tanyakan sesuatu tentang saham ini:")
if question:
    answer = ask_ai(selected_saham, df, question, mode="local")
    st.write(answer)

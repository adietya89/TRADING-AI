import streamlit as st
import plotly.express as px
from utils import prepare_data, model_xgb, features
from chatgpt_integration import ask_ai

st.title("📈 AI Trading Hedge Fund Dashboard")

# =============================
# Pilih saham
# =============================
saham_list = ["BBRI", "BBCA", "BMRI", "TLKM", "ASII", "ADRO", "ANTM"]
selected_saham = st.selectbox("Pilih Saham", saham_list)

# =============================
# Ambil data saham
# =============================
df = prepare_data(selected_saham)
if df is None or df.empty:
    st.error("Data tidak tersedia. Coba saham lain atau periksa koneksi internet.")
    st.stop()

# Debug kolom
st.write("Kolom df:", df.columns.tolist())
st.write("5 baris pertama:", df.head())

# =============================
# Plot grafik Close + MA20 + MA50 + Support/Resistance
# =============================
# Pastikan kolom MA ada
ma_cols = [c for c in ["Close","MA20","MA50"] if c in df.columns]
if not ma_cols:
    st.warning("Tidak ada kolom harga / MA tersedia untuk plotting.")
else:
    df_long = df.melt(id_vars=["Date"], value_vars=ma_cols,
                      var_name="Indicator", value_name="Value")
    support = df['Close'].min()
    resistance = df['Close'].max()
    fig = px.line(df_long, x="Date", y="Value", color="Indicator",
                  title=f"{selected_saham} Chart")
    # Garis support & resistance
    fig.add_hline(y=support, line_dash="dot", line_color="green", annotation_text="Support")
    fig.add_hline(y=resistance, line_dash="dot", line_color="red", annotation_text="Resistance")
    st.plotly_chart(fig)

# =============================
# Prediksi probabilitas naik (dummy)
# =============================
last = df[features].tail(1)
proba = model_xgb.predict_proba(last)[0][1]  # dummy 70%
st.metric("Probabilitas Naik (%)", round(proba*100,2))

# =============================
# AI Lokal Analis Saham
# =============================
st.subheader("🤖 AI Analisis Saham (Lokal)")

ai_mode = st.radio("Mode AI:", ["Local AI"])  # hanya lokal
question = st.text_input("Tanyakan sesuatu tentang saham ini:")

if question:
    answer = ask_ai(selected_saham, df, question, mode="local")
    st.write(answer)

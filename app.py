import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

# Load model & label encoder
model = joblib.load("model_risiko.pkl")
label_encoder = joblib.load("label_encoder.pkl")

# Judul aplikasi
st.set_page_config(page_title="Prediksi Risiko Kredit PNM", layout="wide")
st.title("📊 Prediksi Risiko Kredit Nasabah - PNM")
st.markdown(
    "Masukkan data pinjaman nasabah untuk melihat tingkat **risiko kredit**. "
    "Prediksi ini bisa membantu pengambilan keputusan berdasarkan karakteristik pinjaman mereka."
)

# Sidebar untuk input
st.sidebar.header("📥 Input Data Nasabah")

# Input data manual
out_principal = st.sidebar.number_input("OutStanding Principal (Rp)", min_value=0, step=100000, format="%d")
od_principal = st.sidebar.number_input("OD Principal (Rp)", min_value=0, step=100000, format="%d")
od_interest = st.sidebar.number_input("OD Interest (Rp)", min_value=0, step=100000, format="%d")
disbursed_amount = st.sidebar.number_input("Disbursed Amount (Rp)", min_value=0, step=100000, format="%d")
term = st.sidebar.number_input("Term (Lama Pinjaman)", min_value=1, step=1)
principal_due = st.sidebar.number_input("Principal Due (Rp)", min_value=0, step=100000, format="%d")
interest_due = st.sidebar.number_input("Interest Due (Rp)", min_value=0, step=100000, format="%d")
no_arrear_days = st.sidebar.number_input("Jumlah Hari Menunggak (NoOfArrearDays)", min_value=0, step=1)

# Tombol prediksi
if st.sidebar.button("🔍 Prediksi Risiko"):
    input_data = pd.DataFrame([[
        out_principal, od_principal, od_interest,
        disbursed_amount, term, principal_due,
        interest_due, no_arrear_days
    ]], columns=[
        'OutStandingPrincipal', 'ODPrincipal', 'ODInterest',
        'DisbursedAmount', 'Term', 'PrincipalDue',
        'InterestDue', 'NoOfArrearDays'
    ])

    prediction = model.predict(input_data)[0]
    prediction_label = label_encoder.inverse_transform([prediction])[0]

    # Tampilkan hasil prediksi
    st.success(f"🧾 Hasil Prediksi: **{prediction_label}** Risiko Kredit")

    # Insight Dashboard Section
    st.markdown("### 📈 Insight Risiko Kredit")

    # Dashboard simulasi insight (kamu bisa sesuaikan kalau punya data history)
    risk_map = {
        'Rendah': "✅ Nasabah tergolong aman, dapat dipertimbangkan untuk pengajuan baru.",
        'Sedang': "⚠️ Perlu pemantauan, review histori pembayaran dan kondisi ekonomi nasabah.",
        'Tinggi': "❌ Hindari pemberian pinjaman tambahan. Tinjau ulang profil risiko dan histori kredit."
    }

    st.info(risk_map.get(prediction_label, "Risiko tidak dikenali"))

    # Grafik dummy risiko berdasarkan jumlah hari tunggakan
    st.markdown("#### 📊 Simulasi Dampak Hari Menunggak terhadap Risiko")
    sim_data = pd.DataFrame({
        "Hari Tunggakan": list(range(0, 61, 5)),
        "Skor Risiko (%)": [min(100, i*2 + (10 if prediction_label == 'Tinggi' else 0)) for i in range(13)]
    })
    fig = px.line(sim_data, x="Hari Tunggakan", y="Skor Risiko (%)", markers=True)
    st.plotly_chart(fig, use_container_width=True)


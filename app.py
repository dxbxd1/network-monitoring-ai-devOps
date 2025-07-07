import streamlit as st
import pandas as pd
import os

# إعداد الصفحة (يجب أن يكون أول أمر)
st.set_page_config(
    page_title="Network Monitoring - STC Theme",
    page_icon="🌐",
    layout="wide"
)

# ✅ CSS شامل (خلفية + خط + أزرار + ألوان STC)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Tajawal', sans-serif;
        background-color: #2c004d;
        color: #ffffff;
    }

    .stApp {
        background-color: #2c004d;
        color: #ffffff;
    }

    h1, h2, h3 {
        font-family: 'Tajawal', sans-serif;
        color: #e0c3fc;
    }

    .stButton>button {
        background-color: #500778;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5em 1em;
        font-weight: bold;
    }

    .stButton>button:hover {
        background-color: #b10074;
        color: white;
    }

    .stAlert {
        border-left: 6px solid #b10074;
        background-color: #3a005e;
        color: #ffffff;
    }

    .stDataFrame table {
        color: #ffffff !important;
    }

    /* ✅ درون متحرك */
    .drone-fly {
        position: relative;
        width: 150px;
        animation: fly 4s ease-in-out infinite alternate;
        margin: 0 auto;
        display: block;
    }

    @keyframes fly {
        0%   { transform: translateY(0px) rotate(-2deg); }
        100% { transform: translateY(30px) rotate(2deg); }
    }
    </style>

    <img class="drone-fly" src="https://i.ibb.co/NF3ShpL/drone.png" alt="Drone Flying"/>
""", unsafe_allow_html=True)

# ✅ العبارة الترحيبية
st.markdown("<h1 style='text-align:center;'>Welcome to Eng Mojtaba Badawi Project 🚀</h1>", unsafe_allow_html=True)
st.markdown("---")

# ✅ عنوان التطبيق
st.title("🌐 مراقبة أداء الشبكة - AI Network Monitoring")

# ✅ تحميل البيانات
DATA_PATH = "data/network_data.csv"

if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH)

    st.subheader("📊 آخر 5 قراءات:")
    st.dataframe(df.tail(5), use_container_width=True)

    st.subheader("⚙ المؤشرات الحالية:")
    last = df.iloc[-1]

    col1, col2, col3 = st.columns(3)
    col1.metric("RTT Avg (ms)", round(last["rtt_avg_ms"], 2))
    col2.metric("Download (Mbps)", last["download_mbps"])
    col3.metric("Upload (Mbps)", last["upload_mbps"])

    col4, col5 = st.columns(2)
    col4.metric("Jitter (ms)", last["jitter_ms"])
    col5.metric("Packet Loss (%)", round(last["packet_loss"] * 100, 2))

    st.subheader("🚨 تنبيهات الشبكة:")

    if last["packet_loss"] > 0:
        st.error("⚠ يوجد فقد في الحزم! الشبكة غير مستقرة.")
    elif last["jitter_ms"] > 20:
        st.warning("🔁 الجيتر مرتفع! قد يسبب تقطع بالصوت أو الفيديو.")
    else:
        st.success("✅ أداء الشبكة مستقر حتى الآن.")

    st.subheader("📈 تغير الأداء بمرور الوقت:")
    with st.expander("عرض الرسوم البيانية"):
        chart_cols = st.columns(2)
        with chart_cols[0]:
            st.line_chart(df[["rtt_avg_ms", "jitter_ms"]])
        with chart_cols[1]:
            st.line_chart(df[["download_mbps", "upload_mbps"]])

else:
    st.warning("⚠ لم يتم العثور على ملف البيانات (network_data.csv).")
import streamlit as st
import pandas as pd
import os

# إعدادات الصفحة
st.set_page_config(page_title="Network Monitor", page_icon="🌐", layout="wide")
st.title("🌐 مراقبة أداء الشبكة - AI Network Monitoring")

# مسار البيانات
DATA_PATH = "data/network_data.csv"

if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH)

    st.subheader("📊 آخر 5 قراءات:")
    st.dataframe(df.tail(5), use_container_width=True)

    # ----------- مؤشرات الأداء -----------
    st.subheader("⚙ المؤشرات الحالية:")

    last = df.iloc[-1]
    col1, col2, col3 = st.columns(3)
    col1.metric("RTT Avg (ms)", round(last["rtt_avg_ms"], 2))
    col2.metric("Download (Mbps)", last["download_mbps"])
    col3.metric("Upload (Mbps)", last["upload_mbps"])

    col4, col5 = st.columns(2)
    col4.metric("Jitter (ms)", last["jitter_ms"])
    col5.metric("Packet Loss (%)", round(last["packet_loss"] * 100, 2))

    # ----------- تنبيهات داخلية -----------
    st.subheader("🚨 تنبيهات الشبكة:")

    if last["packet_loss"] > 0:
        st.error("⚠ يوجد فقد في الحزم! الشبكة غير مستقرة.")
    elif last["jitter_ms"] > 20:
        st.warning("🔁 الجيتر مرتفع! قد يسبب تقطع بالصوت أو الفيديو.")
    else:
        st.success("✅ أداء الشبكة مستقر حتى الآن.")

    # ----------- رسم مخططات -----------
    st.subheader("📈 تغير الأداء بمرور الوقت:")

    with st.expander("عرض الرسوم البيانية"):
        chart_cols = st.columns(2)
        with chart_cols[0]:
            st.line_chart(df[["rtt_avg_ms", "jitter_ms"]])
        with chart_cols[1]:
            st.line_chart(df[["download_mbps", "upload_mbps"]])

else:
    st.warning("⚠ لم يتم العثور على ملف البيانات (network_data.csv).")
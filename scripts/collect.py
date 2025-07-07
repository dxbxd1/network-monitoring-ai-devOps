import time
import pandas as pd
from pingparsing import PingParsing, PingTransmitter
import speedtest
import psutil
from datetime import datetime
import requests

# الهدف الذي نستخدمه للاختبار (جوجل)
target = "8.8.8.8"

# مكونات البينق
ping_parser = PingParsing()
ping_transmitter = PingTransmitter()
ping_transmitter.destination = target
ping_transmitter.count = 4

# بيانات التليجرام - عبيهم بقيمك
TELEGRAM_BOT_TOKEN = "7267450606:AAFQkWL0_lDXSWCDWGqF9zHkvWDyiyLNXZE"
TELEGRAM_CHAT_ID = 658534156

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print(f"Failed to send message: {response.text}")
    except Exception as e:
        print(f"Exception during Telegram send: {e}")

def get_network_data():
    # بيانات البينق
    result = ping_transmitter.ping()
    ping_data = ping_parser.parse(result).as_dict()

    # بيانات السرعة
    st = speedtest.Speedtest()
    st.get_best_server()
    download_speed = round(st.download() / 1_000_000, 2)  # Mbps
    upload_speed = round(st.upload() / 1_000_000, 2)

    # بيانات الشبكة المحلية
    net_io = psutil.net_io_counters()

    data = {
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "rtt_avg_ms": ping_data["rtt_avg"],
        "packet_loss": ping_data["packet_loss_rate"],
        "jitter_ms": round(ping_data["rtt_max"] - ping_data["rtt_min"], 2),
        "download_mbps": download_speed,
        "upload_mbps": upload_speed,
        "bytes_sent": net_io.bytes_sent,
        "bytes_recv": net_io.bytes_recv
    }

    # شرط التنبيه: يرسل دائماً للتجربة
    if data["packet_loss"] >= 0 or data["jitter_ms"] >= 20:
        alert_msg = (
            f"🚨 تنبيه شبكة (اختبار)!\n"
            f"🕒 الوقت: {data['timestamp']}\n"
            f"⏱ RTT متوسط: {data['rtt_avg_ms']} ms\n"
            f"📉 فقد الحزم: {round(data['packet_loss'] * 100, 2)}%\n"
            f"🔁 الجيتر: {data['jitter_ms']} ms\n"
            f"⬇ تحميل: {data['download_mbps']} Mbps\n"
            f"⬆ رفع: {data['upload_mbps']} Mbps"
        )
        send_telegram_message(alert_msg)

    return data

# التجميع وحفظ البيانات
def collect_loop(interval=1, duration=2):  # فترة قصيرة للتجربة
    df = pd.DataFrame()
    for _ in range(duration):
        try:
            data = get_network_data()
            df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
            print("✅ Data collected:", data)
        except Exception as e:
            print("❌ Error:", e)
        time.sleep(interval)

    df.to_csv("data/network_data.csv", index=False)
    print("📁 Saved to data/network_data.csv")

# التصحيح هنا
if __name__ == "__main__":
    collect_loop()
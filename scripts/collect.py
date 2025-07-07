import time
import pandas as pd
from pingparsing import PingParsing, PingTransmitter
import speedtest
import psutil
from datetime import datetime

# الهدف الذي نستخدمه للاختبار (جوجل)
target = "8.8.8.8"

# مكونات البينق
ping_parser = PingParsing()
ping_transmitter = PingTransmitter()
ping_transmitter.destination = target
ping_transmitter.count = 4

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

    return data

# التجميع وحفظ البيانات
def collect_loop(interval=10, duration=3):
    df = pd.DataFrame()
    for _ in range(duration):
        try:
            data = get_network_data()
            df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
            print("✅ Data collected:", data)
        except Exception as e:
            print("❌ Error:", e)
        time.sleep(interval)

    df.to_csv("network_data.csv", index=False)
    print("📁 Saved to network_data.csv")

# شغّل التجميع كل 60 ثانية لمدة 10 مرات
if __name__ == "__main__":
    collect_loop(interval=10, duration=3)

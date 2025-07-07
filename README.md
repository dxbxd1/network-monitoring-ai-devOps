# 🚦 Network Monitoring AI + DevOps

نظام ذكي لمراقبة جودة الشبكة وتحليل أدائها باستخدام الذكاء الاصطناعي، ويدعم التكامل مع تقنيات الـ DevOps وCI/CD.

## 📌 نبذة

هذا المشروع يهدف إلى مراقبة الشبكة من خلال:

- تحليل *الـ Ping وJitter وPacket Loss*
- اختبار سرعة الإنترنت (Download/Upload)
- جمع البيانات وتحليلها بشكل دوري
- حفظ النتائج في ملف CSV
- التحضير لواجهة تفاعلية بـ Streamlit وتنبيهات ذكية عبر Email وTelegram

---

## 🧠 التقنية المستخدمة

- Python 3.10
- pandas
- pingparsing
- speedtest-cli
- psutil
- Git + GitHub
- GitHub Actions (قريبًا)
- Streamlit (قريبًا)

---

## ⚙ تشغيل المشروع

```bash
# من داخل scripts/
python collect.py 
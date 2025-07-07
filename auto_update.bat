@echo off
echo [1/4] تشغيل سكريبت جمع البيانات...
python scripts\collect.py

echo [2/4] إضافة البيانات إلى Git...
git add data\network_data.csv

echo [3/4] تنفيذ Commit للتغييرات...
git commit -m "Auto update network data"

echo [4/4] رفع التغييرات إلى GitHub...
git push origin main

echo --- تم التحديث بنجاح! ---
pause
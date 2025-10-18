📘 DEPLOYMENT STEPS – SSK-XAUUSD Momentum Predictor

1️⃣ Go to https://streamlit.io/cloud and log in.
2️⃣ Click “New app”.
3️⃣ Upload this zip: SSK_XAUUSD_StreamlitApp.zip
4️⃣ Wait 1–2 minutes; the app will auto-build and launch.

After launch:
- Turn ON the checkbox “Start Predictive Engine”.
- It will fetch live XAUUSD data every 5 min.
- Browser toast alerts show BUY/SELL signals with confidence %.

To adjust refresh rate → edit `time.sleep(60 * 5)` in app.py.
To switch to 30-min window → change dropdown to “30m”.
──────────────────────────────────────────
🟢 Balanced Mode = ±0.10 %
🔴 Conservative Mode = ±0.15 %
──────────────────────────────────────────

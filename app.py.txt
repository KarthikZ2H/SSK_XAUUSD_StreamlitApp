import streamlit as st
from momentum_engine import get_live_data
from momentum_model import generate_signal
import time

st.set_page_config(page_title="SSK-XAUUSD Momentum Predictor", layout="centered")

st.title("🟡 SSK-XAUUSD Momentum Predictor")
st.markdown("---")

# Controls
mode = st.selectbox("Mode", ["Balanced", "Conservative"], index=0)
interval = st.selectbox("Prediction Window", ["15m", "30m"])
threshold = 0.10 if mode == "Balanced" else 0.15
run_engine = st.checkbox("Start Predictive Engine")

placeholder = st.empty()
log_area = st.container()

if run_engine:
    st.success(f"Engine running in **{mode}** mode | Threshold ±{threshold:.2f}%")
    while run_engine:
        try:
            df = get_live_data(interval)
            signal = generate_signal(df, threshold)
            with placeholder.container():
                st.markdown(f"### {signal['status_icon']} {signal['signal_type']} Signal")
                st.write(f"**Price:** {signal['price']}  |  **Confidence:** {signal['confidence']}%")
                st.write(f"**Target:** {signal['target']}  |  **Stop:** {signal['stop_loss']}")
                st.write(f"**Trend:** {signal['trend']}  |  **Interval:** {interval}")
                st.progress(signal['confidence'] / 100)
            log_area.markdown(f"- {time.strftime('%H:%M:%S')} → {signal['signal_type']} @ {signal['price']} | Conf {signal['confidence']}%")
            st.toast(f"{signal['status_icon']} {signal['signal_type']} {signal['price']} → Target {signal['target']} | Conf {signal['confidence']}%", icon=signal['status_icon'])
            time.sleep(60 * 5)  # 5-min refresh
        except Exception as e:
            st.error(f"Error: {e}")
            time.sleep(60)
else:
    st.info("☝️ Turn on 'Start Predictive Engine' to begin live momentum tracking.")

import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime

# -------------------------------------------------------------
# XAUUSD Momentum Prediction Engine (Balanced / Conservative)
# -------------------------------------------------------------

def fetch_data(symbol="XAUUSD", interval="15m", limit=100):
    """Fetch latest OHLC data from TradingView public API (or any compatible endpoint)."""
    try:
        url = f"https://api.taapi.io/candles?secret=demo&exchange=binance&symbol={symbol}&interval={interval}&limit={limit}"
        res = requests.get(url)
        data = res.json().get("candles", [])
        df = pd.DataFrame(data)
        if df.empty:
            return None
        df["time"] = pd.to_datetime(df["timestamp"], unit="s")
        df = df[["time", "open", "high", "low", "close"]]
        return df
    except Exception as e:
        st.error(f"⚠️ Data fetch error: {e}")
        return None


def compute_momentum(df):
    """Compute RSI and short-term momentum bias."""
    if df is None or len(df) < 2:
        return None, "⚠️ Not enough data yet."

    try:
        df["change"] = df["close"].diff()
        gain = df["change"].where(df["change"] > 0, 0)
        loss = -df["change"].where(df["change"] < 0, 0)
        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()
        rs = avg_gain / avg_loss
        df["rsi"] = 100 - (100 / (1 + rs))

        last_rsi = df["rsi"].iloc[-1]
        last_close = df["close"].iloc[-1]
        prev_close = df["close"].iloc[-2]

        bias = ""
        if last_rsi > 60 and last_close > prev_close:
            bias = "BUY"
        elif last_rsi < 40 and last_close < prev_close:
            bias = "SELL"
        else:
            bias = "NEUTRAL"

        return bias, f"RSI: {last_rsi:.2f}"
    except Exception as e:
        return None, f"⚠️ Computation error: {e}"


def run_engine(mode="Balanced", interval="15m"):
    """Main prediction engine loop."""
    st.subheader("🔁 Live Engine Status")

    df = fetch_data("OANDA:XAUUSD", interval)
    if df is None or len(df) < 2:
        st.error("⚠️ Data temporarily unavailable. Waiting for next candle update.")
        return

    bias, info = compute_momentum(df)

    if bias is None:
        st.warning(info)
        return

    threshold = 0.10 if mode == "Balanced" else 0.05
    st.success(f"Engine running in {mode} mode | Threshold ±{threshold:.2f}%")
    st.info(f"Momentum signal → {bias} | {info}")


# Streamlit UI ------------------------------------------------
def main():
    st.title("🟡 SSK-XAUUSD Momentum Predictor")

    mode = st.selectbox("Mode", ["Balanced", "Conservative"])
    interval = st.selectbox("Prediction Window", ["15m", "30m"])
    start = st.checkbox("Start Predictive Engine")

    if start:
        run_engine(mode, interval)
    else:
        st.warning("🕓 Engine is stopped. Enable it to start live prediction.")


if __name__ == "__main__":
    main()

import pandas as pd

def generate_signal(df, threshold=0.10):
    close = df['close']
    df['ema_fast'] = close.ewm(span=20, adjust=False).mean()
    df['ema_slow'] = close.ewm(span=50, adjust=False).mean()
    df['rsi'] = compute_rsi(close)

    price = round(close.iloc[-1], 2)
    ema_fast = df['ema_fast'].iloc[-1]
    ema_slow = df['ema_slow'].iloc[-1]
    rsi = df['rsi'].iloc[-1]

    trend = "Bullish" if ema_fast > ema_slow else "Bearish"
    diff_pct = abs((ema_fast - ema_slow) / price) * 100
    confidence = min(100, round((diff_pct / threshold) * 50 + (abs(rsi - 50) / 50) * 50, 1))

    if ema_fast > ema_slow and rsi > 55:
        signal_type, icon = "BUY", "🟢"
        target = round(price * (1 + threshold / 100), 2)
        stop_loss = round(price * (1 - threshold / 200), 2)
    elif ema_fast < ema_slow and rsi < 45:
        signal_type, icon = "SELL", "🔴"
        target = round(price * (1 - threshold / 100), 2)
        stop_loss = round(price * (1 + threshold / 200), 2)
    else:
        signal_type, icon = "HOLD", "⚪"
        target, stop_loss = "-", "-"

    return {
        "signal_type": signal_type,
        "status_icon": icon,
        "price": price,
        "target": target,
        "stop_loss": stop_loss,
        "confidence": confidence,
        "trend": trend
    }

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

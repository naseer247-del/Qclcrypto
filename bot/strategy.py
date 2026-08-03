def ema(series, length):
    return series.ewm(span=length, adjust=False).mean()

def rsi(series, length):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(length).mean()
    avg_loss = loss.rolling(length).mean()
    rs = avg_gain / avg_loss.replace(0, 1e-10)
    return 100 - (100 / (1 + rs))

def atr(df, length=14):
    high, low, close = df["high"], df["low"], df["close"]
    prev_close = close.shift(1)
    tr = pd.concat([
        high - low,
        (high - prev_close).abs(),
        (low - prev_close).abs()
    ], axis=1).max(axis=1)
    return tr.rolling(length).mean()

import pandas as pd

def generate_signal(df, cfg):
    df["ema_fast"] = ema(df["close"], cfg["ema_fast"])
    df["ema_slow"] = ema(df["close"], cfg["ema_slow"])
    df["rsi"] = rsi(df["close"], cfg["rsi_period"])
    df["atr"] = atr(df, 14)
    df = df.dropna().reset_index(drop=True)
    if len(df) < 2:
        return "HOLD", df

    prev, curr = df.iloc[-2], df.iloc[-1]
    cross_up = prev["ema_fast"] <= prev["ema_slow"] and curr["ema_fast"] > curr["ema_slow"]
    cross_down = prev["ema_fast"] >= prev["ema_slow"] and curr["ema_fast"] < curr["ema_slow"]

    if cross_up and curr["rsi"] <= cfg["rsi_buy_max"]:
        return "BUY", df
    if cross_down and curr["rsi"] >= cfg["rsi_sell_min"]:
        return "SELL", df
    return "HOLD", df

import pandas_ta as ta

def generate_signal(df, cfg):
    df["ema_fast"] = ta.ema(df["close"], length=cfg["ema_fast"])
    df["ema_slow"] = ta.ema(df["close"], length=cfg["ema_slow"])
    df["rsi"] = ta.rsi(df["close"], length=cfg["rsi_period"])
    df["atr"] = ta.atr(df["high"], df["low"], df["close"], length=14)
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

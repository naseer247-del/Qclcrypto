import json
import os
import yaml
from datetime import datetime, timezone
from exchange import Exchange
from strategy import generate_signal
from risk import position_size, daily_loss_exceeded, stop_loss_price, take_profit_price
from telegram_alert import send

CFG_PATH = os.path.join(os.path.dirname(__file__), "..", "config.yaml")

def load_cfg():
    with open(CFG_PATH) as f:
        return yaml.safe_load(f)

def load_state(path):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {"position": None, "day_start_balance": None, "day": None, "enabled": True}

def save_state(path, state):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(state, f, indent=2)

def main():
    cfg = load_cfg()
    state_path = os.path.join(os.path.dirname(__file__), "..", cfg["state_file"])
    state = load_state(state_path)

    if not state.get("enabled", True):
        send("Bot disabled. Skipping cycle.")
        return

    ex = Exchange(cfg["exchange"])
    balance = ex.get_balance_usdt()

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if state.get("day") != today:
        state["day"] = today
        state["day_start_balance"] = balance

    if daily_loss_exceeded(state, balance, cfg["risk"]):
        send(f"Daily loss limit hit. Trading paused for today. Balance: {balance:.2f}")
        save_state(state_path, state)
        return

    df = ex.fetch_ohlcv()
    signal, df = generate_signal(df, cfg["strategy"])
    price = df.iloc[-1]["close"]
    atr = df.iloc[-1]["atr"]

    pos = state.get("position")

    if pos is None and signal == "BUY":
        qty = position_size(balance, price, atr, cfg["risk"])
        if qty > 0:
            ex.market_buy(qty)
            sl = stop_loss_price(price, atr, cfg["risk"], "long")
            tp = take_profit_price(price, atr, cfg["risk"], "long")
            state["position"] = {"side": "long", "entry": price, "qty": qty, "sl": sl, "tp": tp}
            send(f"BUY {qty:.6f} @ {price:.2f} | SL {sl:.2f} | TP {tp:.2f}")

    elif pos is not None:
        side = pos["side"]
        hit_sl = price <= pos["sl"] if side == "long" else price >= pos["sl"]
        hit_tp = price >= pos["tp"] if side == "long" else price <= pos["tp"]
        exit_signal = signal == "SELL" if side == "long" else signal == "BUY"

        if hit_sl or hit_tp or exit_signal:
            ex.market_sell(pos["qty"])
            reason = "SL" if hit_sl else "TP" if hit_tp else "SIGNAL"
            send(f"SELL {pos['qty']:.6f} @ {price:.2f} | reason {reason}")
            state["position"] = None

    save_state(state_path, state)

if __name__ == "__main__":
    main()

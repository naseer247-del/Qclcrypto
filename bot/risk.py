def position_size(balance, price, atr, cfg):
    risk_amount = balance * (cfg["risk_per_trade_pct"] / 100)
    stop_distance = atr * cfg["stop_loss_atr_mult"]
    if stop_distance <= 0:
        return 0
    qty = risk_amount / stop_distance
    max_qty_by_balance = balance / price
    return min(qty, max_qty_by_balance)

def daily_loss_exceeded(state, balance, cfg):
    start_balance = state.get("day_start_balance", balance)
    loss_pct = (start_balance - balance) / start_balance * 100
    return loss_pct >= cfg["max_daily_loss_pct"]

def stop_loss_price(entry, atr, cfg, side):
    dist = atr * cfg["stop_loss_atr_mult"]
    return entry - dist if side == "long" else entry + dist

def take_profit_price(entry, atr, cfg, side):
    dist = atr * cfg["take_profit_atr_mult"]
    return entry + dist if side == "long" else entry - dist

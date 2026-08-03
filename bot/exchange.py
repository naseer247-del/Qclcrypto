import os
import ccxt
import pandas as pd

class Exchange:
    def __init__(self, cfg):
        self.symbol = cfg["symbol"]
        self.timeframe = cfg["timeframe"]
        klass = getattr(ccxt, cfg["name"])
        self.client = klass({
            "apiKey": os.environ.get("EXCHANGE_API_KEY"),
            "secret": os.environ.get("EXCHANGE_API_SECRET"),
            "enableRateLimit": True,
        })
        if cfg.get("testnet"):
            self.client.set_sandbox_mode(True)

    def fetch_ohlcv(self, limit=200):
        raw = self.client.fetch_ohlcv(self.symbol, timeframe=self.timeframe, limit=limit)
        df = pd.DataFrame(raw, columns=["ts", "open", "high", "low", "close", "volume"])
        df["ts"] = pd.to_datetime(df["ts"], unit="ms")
        return df

    def get_balance_usdt(self):
        bal = self.client.fetch_balance()
        return bal.get("USDT", {}).get("free", 0)

    def market_buy(self, amount):
        return self.client.create_market_buy_order(self.symbol, amount)

    def market_sell(self, amount):
        return self.client.create_market_sell_order(self.symbol, amount)

    def last_price(self):
        return self.client.fetch_ticker(self.symbol)["last"]

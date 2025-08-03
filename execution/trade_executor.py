import time
import pandas as pd
from binance.client import Client
from utils.config import BINANCE_API_KEY, BINANCE_API_SECRET

client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)

def execute_trade(symbol, side, quantity):
    try:
        order = client.create_order(
            symbol=symbol,
            side=side.upper(),
            type="MARKET",
            quantity=quantity
        )
        print(f"Executed {side} trade for {quantity} {symbol}: {order['fills'][0]['price']}")
    except Exception as e:
        print(f"Trade failed for {symbol}: {e}")

def simulate_trades(df, threshold=1.0):
    for _, row in df.iterrows():
        if abs(row["score"]) >= threshold:
            side = "BUY" if row["score"] > 0 else "SELL"
            symbol = row["symbol"]
            execute_trade(symbol.replace("USDT", ""), side, 10)  # Simulate 10 units
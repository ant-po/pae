import sqlite3
import duckdb
import pandas as pd
from utils.config import SQLITE_DB

def backtest_impulse_strategy():
    con = sqlite3.connect(SQLITE_DB)
    df = pd.read_sql("SELECT * FROM signals", con, parse_dates=["timestamp"])
    df["pnl"] = df["ret"] * 0.99  # Assume 1% slippage
    df["cumpnl"] = df["pnl"].cumsum()
    con.close()
    return df

if __name__ == "__main__":
    df = backtest_impulse_strategy()
    print(df[["timestamp", "symbol", "ret", "pnl", "cumpnl"]].tail())
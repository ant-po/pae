import pandas as pd
import numpy as np
from utils.config import DATA_DIR

def detect_btc_impulses(thresh_pct=0.5):
    btc = pd.read_csv(f"{DATA_DIR}/BTCUSDT.csv", parse_dates=["timestamp"])
    btc["ret"] = btc["close"].pct_change() * 100
    impulses = btc[btc["ret"].abs() > thresh_pct].copy()
    impulses = impulses[["timestamp", "ret"]]
    impulses["direction"] = np.where(impulses["ret"] > 0, "up", "down")
    return impulses

def score_signal(impulse_ret, alt_ret):
    raw_score = alt_ret * np.sign(impulse_ret)
    magnitude_bonus = np.log1p(abs(impulse_ret))
    return raw_score * magnitude_bonus

def evaluate_alt_lag(symbol, impulses):
    alt = pd.read_csv(f"{DATA_DIR}/{symbol}.csv", parse_dates=["timestamp"])
    alt["ret"] = alt["close"].pct_change() * 100
    results = []
    for _, row in impulses.iterrows():
        t0 = row["timestamp"]
        t1 = t0 + pd.Timedelta(minutes=5)
        after = alt[(alt["timestamp"] > t0) & (alt["timestamp"] <= t1)]
        if not after.empty:
            net_ret = after["ret"].sum()
            score = score_signal(row["ret"], net_ret)
            results.append({
                "timestamp": t0,
                "symbol": symbol,
                "ret": net_ret,
                "btc_dir": row["direction"],
                "score": score
            })
    return pd.DataFrame(results)
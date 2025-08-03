from strategies.impulse_diffusion.signal import detect_btc_impulses, evaluate_alt_lag
from storage.sqlite_logger import init_db, log_signals
from utils.config import SYMBOLS

init_db()
impulses = detect_btc_impulses(thresh_pct=0.4)
results = []
for sym in SYMBOLS:
    if sym != "BTCUSDT":
        df = evaluate_alt_lag(sym, impulses)
        df = df[df["score"].abs() > 0.5]  # Filter by score threshold
        results.append(df)
if results:
    final_df = pd.concat(results)
    log_signals(final_df)
    print(final_df.sort_values("score", ascending=False).head())
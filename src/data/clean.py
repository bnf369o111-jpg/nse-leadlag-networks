from pathlib import Path

import numpy as np
import pandas as pd
import yaml

cfg = yaml.safe_load(open("config.yaml"))
prices = pd.read_parquet("data/raw/prices.parquet")

close = prices.xs("Close", axis=1, level=1).sort_index()
volume = prices.xs("Volume", axis=1, level=1).sort_index()

close = close.dropna(how="all")              # drop exchange holidays
log_ret = np.log(close).diff().iloc[1:]      # NO forward-fill: missing stays missing

bench = log_ret.pop(cfg["benchmark"])
volume = volume.drop(columns=cfg["benchmark"], errors="ignore")

coverage = log_ret.notna().mean()
traded_value_cr = (close[log_ret.columns] * volume[log_ret.columns]).median() / 1e7
spike_days = (log_ret.abs() > cfg["max_abs_log_return"]).sum()

keep = (coverage >= cfg["min_history_frac"]) & \
       (traded_value_cr >= cfg["min_median_traded_value_cr"])

report = pd.DataFrame({"coverage": coverage.round(3),
                       "median_traded_value_cr": traded_value_cr.round(1),
                       "spike_days": spike_days,
                       "kept": keep}).sort_values("kept")

out_dir = Path("data/processed")
out_dir.mkdir(parents=True, exist_ok=True)
report.to_csv(out_dir / "quality_report.csv")
log_ret.loc[:, keep].to_parquet(out_dir / "log_returns.parquet")
bench.to_frame("nifty50").to_parquet(out_dir / "benchmark.parquet")

print(f"kept {keep.sum()} of {len(keep)} stocks over {len(log_ret)} days")
print(report[report.spike_days > 0])
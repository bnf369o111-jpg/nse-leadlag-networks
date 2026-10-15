import time
from pathlib import Path

import pandas as pd
import yaml
import yfinance as yf

cfg = yaml.safe_load(open("config.yaml"))
raw_dir = Path("data/raw")
raw_dir.mkdir(parents=True, exist_ok=True)

universe = pd.read_csv(cfg["universe_file"])
tickers = [s.strip() + ".NS" for s in universe["Symbol"]] + [cfg["benchmark"]]

frames = []
for i in range(0, len(tickers), 50):
    batch = tickers[i:i + 50]
    df = yf.download(batch, start=cfg["start"], end=cfg["end"],
                     auto_adjust=True, group_by="ticker",
                     progress=False, threads=True)
    frames.append(df)
    print(f"downloaded {i + len(batch)}/{len(tickers)}")
    time.sleep(2)

prices = pd.concat(frames, axis=1)
prices.to_parquet(raw_dir / "prices.parquet")
print(prices.shape)
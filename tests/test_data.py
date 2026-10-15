import numpy as np
import pandas as pd

def test_returns_are_clean():
    r = pd.read_parquet("data/processed/log_returns.parquet")
    assert r.index.is_monotonic_increasing
    assert not r.index.duplicated().any()
    assert np.isfinite(r.stack()).all()
    assert r.shape[1] >= 100
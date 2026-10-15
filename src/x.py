import pandas as pd 
import numpy as np 
import yaml

prices = pd.read_parquet('data/raw/prices.parquet')
close = prices.xs("Volume", axis=1, level=1).sort_index()


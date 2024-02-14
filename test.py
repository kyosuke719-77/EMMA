import numpy as np
import pandas as pd

df = pd.read_csv('./行動パターン.csv')
arr = df.iloc[:,2:].to_numpy()

print(arr)

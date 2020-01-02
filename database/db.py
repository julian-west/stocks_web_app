import ffn
import pandas as pd

data = ffn.get(['AMAT','LRCX'],start='2019-09-01',end='2019-10-15').reset_index()
data = data.melt(id_vars=['Date'])
print(data)
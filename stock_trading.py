import pandas as pd 
from stock_data import get_symbol_daily_data

df = get_symbol_daily_data(symbol="000060", since='20100101')

want_col = ['stck_bsop_date', 'stck_clpr', 'stck_hgpr', 'stck_lwpr', 'stck_oprc', 'acml_vol', 'acml_tr_pbmn']
df = df[want_col]
df.columns = ['date', 'close', 'high', 'low', 'open', 'volume', 'amount']
df['date'] = pd.to_datetime(df['date'])

df.sort_values('date', ascending=True, inplace=True)
df['ma5'] = df['close'].rolling(window=5).mean()
df['ma20'] = df['close'].rolling(window=20).mean()
df['ma60'] = df['close'].rolling(window=60).mean()
df['ma120'] = df['close'].rolling(window=120).mean()
print(df)
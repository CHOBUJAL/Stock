import pandas as pd 
from stock_data import get_symbol_daily_data

a = get_symbol_daily_data(symbol="000060", since='20100101')

want_col = ['stck_bsop_date', 'stck_clpr', 'stck_hgpr', 'stck_lwpr', 'stck_oprc', 'acml_vol', 'acml_tr_pbmn']
df = a[want_col]
df.columns = ['date', 'close', 'high', 'low', 'open', 'volume', 'amount']
df['date'] = pd.to_datetime(df['date'])
df = df

df.sort_values('date', ascending=True, inplace=True)
df['ma5'] = df['close'].rolling(window=5).mean()
print(df)
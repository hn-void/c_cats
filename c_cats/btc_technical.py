import math
import os

import pandas as pd

import handle_data
import technical


FILE_NAME = 'btc_data/btc_historical.csv'

if not os.path.exists(FILE_NAME):
    df = handle_data.get_historical_from_cryptocompare('BTC', 'JPY')
    print(df)
    df.to_csv(FILE_NAME)
else:
    if not handle_data.is_latest(FILE_NAME):
        df = handle_data.get_historical_from_cryptocompare('BTC', 'JPY')
        df.to_csv(FILE_NAME)

btc_df = pd.read_csv(FILE_NAME)


"""""""""
Edit here, make signals
"""""""""
ima_buy, ima_sell = technical.increasing_mavg(btc_df, short_term=1, long_term=20, band_width=0.01)
bband_buy, bband_sell = technical.bollinger_band(btc_df, term=20, band_width=2)

signal_buy = technical.normalize(ima_buy + bband_buy)
signal_sell = technical.normalize(ima_sell + bband_sell)
signal = signal_buy - signal_sell
"""""""""
Edit here
"""""""""

signal_today = signal.iloc[-1].values[0]
print(signal_today)
if signal_today > 0:
    print('[c_cats]\tYou had better sell', signal_today, 'BTC today')
elif signal_today < 0:
    print('[c_cats]\tYou had better buy', math.fabs(signal_today), 'BTC today')
else:
    print('[c_cats] You don\'t have to trade BTC today')

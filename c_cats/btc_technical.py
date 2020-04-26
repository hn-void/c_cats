import math
import os
import time

import pandas as pd

import handle_data
import technical


os.environ['TZ'] = 'UTC'
time.tzset()

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
macd_buy, macd_sell = technical.ma_convergence_divergence(btc_df, short_term=12, long_term=26)
est_buy, est_sell = technical.ma_estrangement(btc_df, term=25, band_width=0.1)
cci_buy, cci_sell = technical.commodity_channel_index(btc_df, term=21, follower=100, contrarian=200)
rsi_buy, rsi_sell = technical.relative_strength_index(btc_df, term=14, follower=20, contrarian=40)

signal = ima_buy + bband_buy + macd_buy + est_buy + cci_buy + rsi_buy
signal = signal - ima_sell - bband_sell - macd_sell - est_sell - cci_sell - rsi_sell
"""""""""
Edit here
"""""""""

signal_today = signal.iloc[-1].values[0]
print(signal_today)
if signal_today > 0:
    print('[c_cats]\tYou had better buy', signal_today, 'BTC today')
elif signal_today < 0:
    print('[c_cats]\tYou had better sell', math.fabs(signal_today), 'BTC today')
else:
    print('[c_cats] You don\'t have to trade BTC today')

import math
import os
import time

import pandas as pd

from btc_utils import handle_data, simulation, technical


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
Edit here, signal, secure_profit, stop_loss
"""""""""
ima_buy, ima_sell = technical.increasing_mavg(btc_df, short_term=1, long_term=20, band_width=0.01)
bband_buy, bband_sell = technical.bollinger_band(btc_df, term=20, band_width=2)
macd_buy, macd_sell = technical.ma_convergence_divergence(btc_df, short_term=12, long_term=26)
est_buy, est_sell = technical.ma_estrangement(btc_df, term=25, band_width=0.1)
cci_buy, cci_sell = technical.commodity_channel_index(btc_df, term=21, follower=100, contrarian=200)
rsi_buy, rsi_sell = technical.relative_strength_index(btc_df, term=14, follower=20, contrarian=40)

# Sample Signal 1
# signal_df = ima_buy + bband_buy + macd_buy + est_buy + cci_buy + rsi_buy
# signal_df = signal_df - ima_sell - bband_sell - macd_sell - est_sell - cci_sell - rsi_sell
# signal_df[(signal_df <= 1.0) & (signal_df >= -1.0)] = 0.0
# signal_df[signal_df > 1.0] = 2.0
# signal_df[signal_df < -1.0] = -2.0

# Sample Signal 2
# signal_df = ima_buy + est_buy + rsi_buy - bband_sell - cci_sell - macd_sell

# Sample Signal 3
signal_df = macd_buy - macd_sell
secure_profit = 0.05
stop_loss = -0.03
transaction_fee_ratio = 0.01

"""""""""
Edit here
"""""""""

print('-'*80)
simulation.simulate(
    10000000,
    btc_df=btc_df,
    signal_df=signal_df,
    stop_loss=stop_loss,
    secure_profit=secure_profit,
    per_transaction_fee_percent=transaction_fee_ratio)
print('-'*80)

signal_today = signal_df.iloc[-1].values[0]
if signal_today > 0:
    print('[c_cats] You had better buy', signal_today, 'BTC today')
elif signal_today < 0:
    print('[c_cats] You had better sell', math.fabs(signal_today), 'BTC today')
else:
    print('[c_cats] You don\'t have to trade BTC today')

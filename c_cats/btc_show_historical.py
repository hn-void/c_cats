import os
import time

import pandas as pd

import handle_data


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

# handle_data.show_historical(btc_df, start_date='2019-01-01', end_date='2020-01-01')
handle_data.show_historical(btc_df)

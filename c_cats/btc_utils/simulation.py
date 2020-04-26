import datetime
import math

import numpy as np
import pandas as pd
from pandas.plotting import register_matplotlib_converters
from matplotlib import pyplot as plt

register_matplotlib_converters()


def simulate(
        start_jpy: int,
        btc_df: pd.DataFrame,
        signal_df: pd.DataFrame,
        start_date='2019-06-01',
        end_date='2020-04-01',
        per_transaction_fee_percent=0.05,
        unit=1.0,
        graph=True
        ):

    btc_df_cp = btc_df.copy()
    btc_df_cp['signal'] = signal_df * unit
    start_index = btc_df[btc_df['timestamp'] == start_date].index.values[0]
    end_index = btc_df[btc_df['timestamp'] == end_date].index.values[0]
    btc_df_cp = btc_df_cp.iloc[start_index:end_index+1]
    btc_df_cp['total'] = 0
    btc_df_cp['buy_and_hold'] = 0
    btc_df_cp['time_id'] = 0

    jpy = start_jpy
    btc = 0.0
    total_assets = start_jpy
    max_btc = jpy // int(btc_df_cp['close'].iloc[0] * (1 + per_transaction_fee_percent))
    remain_jpy = jpy - max_btc * int(btc_df_cp['close'].iloc[0] * (1 + per_transaction_fee_percent))
    for index, row in btc_df_cp.iterrows():
        if row['signal'] > 0:
            if jpy > int(row['signal'] * int(row['close'] * (1 + per_transaction_fee_percent))):
                jpy = jpy - int(row['signal'] * int(row['close'] * (1 + per_transaction_fee_percent)))
                btc = btc + row['signal']
        elif row['signal'] < 0:
            if btc > math.fabs(row['signal']):
                jpy = jpy + int(math.fabs(row['signal']) * int(row['close'] * (1 - per_transaction_fee_percent)))
                btc = btc + row['signal']
        total_assets = jpy+int(btc*int(row['close']))
        buy_and_hold = remain_jpy + max_btc * row['close']
        btc_df_cp.loc[index, 'total'] = total_assets
        btc_df_cp.loc[index, 'buy_and_hold'] = buy_and_hold
        btc_df_cp.loc[index, 'time_id'] = datetime.datetime.fromtimestamp(row['time'])
        print(
            'DATE:', row['timestamp'],
            'PRICE:', row['close'],
            'SIGNAL:', row['signal'],
            'JPY:', jpy,
            'BTC:', btc,
            'TOTAL:', total_assets)
    print('START', 'JPY:', start_jpy, 'BTC:', 0.0, 'TOTAL:', start_jpy)
    print('FINISH', 'JPY:', jpy, 'BTC:', btc, 'TOTAL:', total_assets)
    print('[c_cats] Simulation Result:', (total_assets - start_jpy) / start_jpy * 100, '%')

    if graph:
        plt.plot(btc_df_cp['time_id'], btc_df_cp['total'], label='Your Algorithm')
        plt.plot(btc_df_cp['time_id'], np.full((btc_df_cp.shape[0],), start_jpy), label='Start JPY')
        plt.plot(btc_df_cp['time_id'], btc_df_cp['buy_and_hold'], label='Buy and Hold')
        plt.xlabel('Date')
        plt.ylabel('JPY')
        plt.legend()
        plt.show()

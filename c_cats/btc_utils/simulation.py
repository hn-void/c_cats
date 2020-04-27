from collections import defaultdict
import datetime
import math

import numpy as np
import pandas as pd
from pandas.plotting import register_matplotlib_converters
from matplotlib import pyplot as plt

register_matplotlib_converters()


class BTCRecord:

    def __init__(self):
        # {btc price: btc amount}
        self.btc_dict = defaultdict(float)

    def add_record(self, price, amount):
        if self.btc_dict[price]:
            self.btc_dict[price] += amount
        else:
            self.btc_dict[price] = amount

    def sub_record(self, amount):
        record_sorted = sorted(self.btc_dict.items(), key=lambda x: x[0], reverse=True)
        for key, value in record_sorted:
            if amount == 0.0:
                break
            if value <= amount:
                amount = amount - value
                self.btc_dict[key] = 0.0
            else:
                self.btc_dict[key] = self.btc_dict[key] - amount
                amount = 0.0

    def secure_profit(self, price, ratio):
        if not ratio:
            return 0.0
        amount = 0.0
        record_sorted = sorted(self.btc_dict.items(), key=lambda x: x[0])
        for key, value in record_sorted:
            if (price - key) / key > ratio:
                amount = amount + self.btc_dict[key]
                self.btc_dict[key] = 0.0
        return amount

    def stop_loss(self, price, ratio):
        if not ratio:
            return 0.0
        amount = 0.0
        record_sorted = sorted(self.btc_dict.items(), key=lambda x: x[0])
        for key, value in record_sorted:
            if (price - key) / key < ratio:
                amount = amount + self.btc_dict[key]
                self.btc_dict[key] = 0.0
        return amount

    def print_record(self):
        record_sorted = sorted(self.btc_dict.items(), key=lambda x: x[0])
        print(record_sorted)


def simulate(
        start_jpy: int,
        btc_df: pd.DataFrame,
        signal_df: pd.DataFrame,
        start_date='2019-06-01',
        end_date='2020-04-01',
        per_transaction_fee_percent=0.05,
        unit=1.0,
        graph=True,
        stop_loss=None,
        secure_profit=None,
        ):

    btc_record = BTCRecord()

    btc_df_cp = btc_df.copy()
    btc_df_cp['signal'] = signal_df * unit
    start_index = btc_df[btc_df['timestamp'] == start_date].index.values[0]
    end_index = btc_df[btc_df['timestamp'] == end_date].index.values[0]
    btc_df_cp = btc_df_cp.iloc[start_index:end_index+1]
    btc_df_cp['total'] = 0
    btc_df_cp['buy_and_hold'] = 0
    btc_df_cp['time_id'] = 0

    trading_count = 0
    buy_and_hold = 0
    jpy = start_jpy
    btc = 0.0
    total_assets = start_jpy
    max_btc = jpy // int(btc_df_cp['close'].iloc[0] * (1 + per_transaction_fee_percent))
    remain_jpy = jpy - max_btc * int(btc_df_cp['close'].iloc[0] * (1 + per_transaction_fee_percent))

    for index, row in btc_df_cp.iterrows():

        trading_flag = False
        secure_stop_flag = False

        # flake8 does not support the walrus operator now
        # if stop_loss_amount := btc_record.stop_loss(int(row['close']), stop_loss) > 0.0:
        stop_loss_amount = btc_record.stop_loss(int(row['close']), stop_loss)
        if stop_loss_amount > 0.0:
            jpy = jpy + int(stop_loss_amount * int(row['close'] * (1 - per_transaction_fee_percent)))
            btc = btc - stop_loss_amount
            trading_flag = True
            secure_stop_flag = True
        # if secure_profit_amount := btc_record.secure_profit(int(row['close']), secure_profit) > 0.0:
        secure_profit_amount = btc_record.secure_profit(int(row['close']), secure_profit)
        if secure_profit_amount > 0.0:
            jpy = jpy + int(secure_profit_amount * int(row['close'] * (1 - per_transaction_fee_percent)))
            btc = btc - secure_profit_amount
            trading_flag = True
            secure_stop_flag = True
        if row['signal'] > 0 and not secure_stop_flag:
            if jpy > int(row['signal'] * int(row['close'] * (1 + per_transaction_fee_percent))):
                jpy = jpy - int(row['signal'] * int(row['close'] * (1 + per_transaction_fee_percent)))
                btc = btc + row['signal']
                btc_record.add_record(int(row['close']), row['signal'])
                trading_flag = True
        elif row['signal'] < 0 and not secure_stop_flag:
            if btc > math.fabs(row['signal']):
                jpy = jpy + int(math.fabs(row['signal']) * int(row['close'] * (1 - per_transaction_fee_percent)))
                btc = btc + row['signal']
                btc_record.sub_record(-row['signal'])
                trading_flag = True
        if trading_flag:
            trading_count = trading_count + 1
        total_assets = jpy+int(btc*int(row['close']))
        buy_and_hold = remain_jpy + max_btc * row['close']
        btc_df_cp.loc[index, 'total'] = total_assets
        btc_df_cp.loc[index, 'buy_and_hold'] = buy_and_hold
        btc_df_cp.loc[index, 'time_id'] = datetime.datetime.fromtimestamp(row['time'])
        # btc_record.print_record()
        print(
            'DATE:', row['timestamp'],
            '  PRICE:', row['close'],
            '  SIGNAL:', row['signal'],
            '  STOP_LOSS:', stop_loss_amount,
            '  SECURE_PROFIT:', secure_profit_amount,
            '  JPY:', jpy,
            '  BTC:', btc,
            '  TOTAL:', total_assets,
            sep='')
    print('[START]', '\tJPY:', start_jpy, '\tBTC:', 0.0, '\tTOTAL:', start_jpy)
    print('[BUY-AND-HOLD]', '\tJPY:', remain_jpy, '\tBTC:', max_btc, '\tTOTAL:', buy_and_hold)
    print('[ALGORITHM]', '\tJPY:', jpy, '\tBTC:', btc, '\tTOTAL:', total_assets)
    print(
        '[c_cats] Simulation Result:', (total_assets - start_jpy) / start_jpy * 100, '%',
        '  Trading Count:', trading_count, sep='')

    if graph:
        plt.plot(btc_df_cp['time_id'], btc_df_cp['total'], label='Your Algorithm')
        plt.plot(btc_df_cp['time_id'], np.full((btc_df_cp.shape[0],), start_jpy), label='Start JPY')
        plt.plot(btc_df_cp['time_id'], btc_df_cp['buy_and_hold'], label='Buy and Hold')
        plt.xlabel('Date')
        plt.ylabel('JPY')
        plt.legend()
        plt.show()

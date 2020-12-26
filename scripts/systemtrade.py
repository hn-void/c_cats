import datetime

import pandas as pd
from matplotlib import pyplot as plt

import technical as tec


plt.style.use('ggplot')
FILE_NAME = 'btc2usd.csv'
FROM_DATE = '2020-01-01'
TO_DATE = '2020-12-01'
TO_DATE = None


def trade_with_golden_cross(df, short_term=5, long_term=25, symbol='close'):
    df_mavg_short = tec.mavg(df, short_term)
    df_mavg_long = tec.mavg(df, long_term)
    df_golden = df_mavg_short.copy()
    df_golden['ratio'] = df_mavg_short[symbol] / df_mavg_long[symbol]
    df_golden['ratio_yesterday'] = df_golden['ratio'].shift(1)
    df_golden['buy_signal'] = df_golden.apply(lambda x: x['ratio'] > 1 and x['ratio_yesterday'] < 1, axis=1)
    df_golden = df_golden.drop([symbol], axis=1)
    return df_golden


def trade_with_dead_cross(df, short_term=5, long_term=25, symbol='close'):
    df_mavg_short = tec.mavg(df, short_term)
    df_mavg_long = tec.mavg(df, long_term)
    df_dead = df_mavg_short.copy()
    df_dead['ratio'] = df_mavg_short[symbol] / df_mavg_long[symbol]
    df_dead['ratio_yesterday'] = df_dead['ratio'].shift(1)
    df_dead = df_dead.drop([symbol], axis=1)
    df_dead['sell_signal'] = df_dead.apply(lambda x: x['ratio'] < 1 and x['ratio_yesterday'] > 1, axis=1)
    return df_dead


if __name__ == '__main__':

    df_usd2btc = pd.read_csv(FILE_NAME)
    df_usd2btc['timestamp'] = df_usd2btc['time'].apply(lambda x: datetime.datetime.fromtimestamp(x))
    df_golden = trade_with_golden_cross(df_usd2btc)
    df_dead = trade_with_dead_cross(df_usd2btc)
    print(df_golden)
    print(df_dead)

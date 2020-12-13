import datetime

import pandas as pd
from matplotlib import pyplot as plt

import technical


FILE_NAME = 'btc2usd.csv'


class TechnicalIndicator:

    def __init__(self, df, color=None):
        self.df = df.copy()
        self.color = color


class MavgIndicator(TechnicalIndicator):

    def __init__(self, df, term=26, color=None):
        self.df = technical.mavg(df=df, term=term)
        self.color = color


def show_chart(list_indicators, start_date=None, end_date=None):
    for indicator in list_indicators:
        plt.plot(indicator.df['timestamp'], indicator.df['close'])
    plt.xlabel('Date')
    plt.ylabel('USD/BTC')
    plt.show()


if __name__ == '__main__':

    list_indicators = []

    df_usd2btc = pd.read_csv(FILE_NAME)
    df_usd2btc['timestamp'] = df_usd2btc['time'].apply(lambda x: datetime.datetime.fromtimestamp(x))
    raw_indicator = TechnicalIndicator(df=df_usd2btc)
    list_indicators.append(raw_indicator)

    mavg_indicator = MavgIndicator(df=raw_indicator.df)
    list_indicators.append(mavg_indicator)

    show_chart(list_indicators=list_indicators)

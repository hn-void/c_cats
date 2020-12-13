import datetime

import pandas as pd
from matplotlib import pyplot as plt

import technical as tec


plt.style.use('ggplot')
FILE_NAME = 'btc2usd.csv'
FROM_DATE = '2020-01-01'
# TO_DATE = '2020-12-01'
TO_DATE = None


def show_chart(list_indicators, fdate=None, tdate=None):
    for indicator in list_indicators:
        if fdate:
            indicator.df = indicator.df[indicator.df['timestamp'] > fdate]
        if tdate:
            indicator.df = indicator.df[indicator.df['timestamp'] < tdate]
        if isinstance(indicator, tec.BBandIndicator):
            plt.plot(
                indicator.df['timestamp'],
                indicator.df['upper'],
                label=indicator.name,
                color=indicator.color,
                alpha=indicator.alpha)
            plt.plot(
                indicator.df['timestamp'],
                indicator.df['lower'],
                label=None,
                color=indicator.color,
                alpha=indicator.alpha)
            plt.plot(
                [indicator.df['timestamp'], indicator.df['timestamp']],
                [indicator.df['lower'], indicator.df['upper']],
                label=None,
                color=indicator.color,
                alpha=indicator.subalpha)
        else:
            plt.plot(indicator.df['timestamp'], indicator.df['close'], label=indicator.name, color=indicator.color)
    plt.xlabel('Date')
    plt.ylabel('USD/BTC')
    plt.legend()
    plt.show()


if __name__ == '__main__':

    list_indicators = []
    if FROM_DATE:
        from_date = datetime.datetime.strptime(FROM_DATE, '%Y-%m-%d')
    else:
        from_date = None
    if TO_DATE:
        to_date = datetime.datetime.strptime(TO_DATE, '%Y-%m-%d')
    else:
        to_date = None

    df_usd2btc = pd.read_csv(FILE_NAME)
    df_usd2btc['timestamp'] = df_usd2btc['time'].apply(lambda x: datetime.datetime.fromtimestamp(x))

    raw_indicator = tec.TechnicalIndicator(df=df_usd2btc[['close', 'timestamp']], name='Raw Data')
    mavg_indicator = tec.MavgIndicator(df=raw_indicator.df)
    bband_indicator = tec.BBandIndicator(df=raw_indicator.df, color='c', alpha=0.4)

    list_indicators.append(bband_indicator)
    list_indicators.append(mavg_indicator)
    list_indicators.append(raw_indicator)

    show_chart(list_indicators=list_indicators, fdate=from_date, tdate=to_date)

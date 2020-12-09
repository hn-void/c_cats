import pandas as pd
from matplotlib import pyplot as plt

from btc_utils import technical


FILE_NAME = 'btc_data/btc_historical.csv'

btc_df = pd.read_csv(FILE_NAME)
df_close = btc_df['close'].copy()


if __name__ == '__main__':
    df_mavg = technical.mavg(btc_df, 25)
    print(df_close)
    print(df_mavg)
    plt.plot(df_close)
    plt.plot(df_mavg)
    plt.show()

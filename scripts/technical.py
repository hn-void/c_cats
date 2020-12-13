# Moving Average
def mavg(df, term, symbol='close'):
    df_mavg = df[symbol].copy().to_frame().rolling(window=term).mean().join(df['timestamp'])
    return df_mavg


class TechnicalIndicator:

    def __init__(self, df=None, name=None, color=None):
        self.df = df
        self.name = name
        self.color = color


class MavgIndicator(TechnicalIndicator):

    def __init__(self, df, term=26, color=None):
        self.df = mavg(df=df, term=term)
        self.name = 'Moving Average: term=' + str(term)
        self.color = color

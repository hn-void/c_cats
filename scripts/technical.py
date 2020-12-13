# Moving Average
def mavg(df, term, symbol='close'):
    df_mavg = df[symbol].copy().to_frame().rolling(window=term).mean().join(df['timestamp'])
    return df_mavg


# Bollinger Band
def bband_upper(df, term, symbol='close'):
    df_mavg = df[symbol].copy().to_frame().rolling(window=term).mean()
    df_sigma = df[symbol].copy().to_frame().rolling(window=term).std()
    df_bband_upper = df_mavg + 2 * df_sigma
    df_bband_upper['timestamp'] = df['timestamp']
    return df_bband_upper


def bband_lower(df, term, symbol='close'):
    df_mavg = df[symbol].copy().to_frame().rolling(window=term).mean()
    df_sigma = df[symbol].copy().to_frame().rolling(window=term).std()
    df_bband_lower = df_mavg - 2 * df_sigma
    df_bband_lower['timestamp'] = df['timestamp']
    return df_bband_lower


class TechnicalIndicator:

    def __init__(self, df=None, name=None, color=None, alpha=None):
        self.df = df
        self.name = name
        self.color = color
        self.alpha = alpha


class MavgIndicator(TechnicalIndicator):

    def __init__(self, df, term=26, color=None, alpha=None):
        self.df = mavg(df=df, term=term)
        self.name = 'Moving Average: term=' + str(term)
        self.color = color
        self.alpha = alpha


class BBandUpperIndicator(TechnicalIndicator):
    def __init__(self, df, term=26, color=None, alpha=None):
        self.df = bband_upper(df=df, term=term)
        self.name = 'Bollinger Band Upper: term=' + str(term)
        self.color = color
        self.alpha = alpha


class BBandLowerIndicator(TechnicalIndicator):
    def __init__(self, df, term=26, color=None, alpha=None):
        self.df = bband_lower(df=df, term=term)
        self.name = 'Bollinger Band Lower: term=' + str(term)
        self.color = color
        self.alpha = alpha

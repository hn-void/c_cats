import pandas as pd
import numpy as np


# Used for making signals
def isnull_to_num(df):
    df_cp = df.copy()
    df_cp[~pd.isnull(df_cp)] = 1.0
    df_cp[pd.isnull(df_cp)] = 0.0
    return df_cp


def generate_marketsig(df, th_weak, th_string):
    df_sig = pd.DataFrame(data=0.0, index=df.index, columns=df.columns)
    df_sig[df > th_weak] = 0.5
    df_sig[df < -th_weak] = -0.5
    df_sig[df > th_string] = 1.0
    df_sig[df < -th_string] = -1.0
    return df_sig


def normalize(df):
    df_normalized = df.copy()
    df_max = df.max()
    df_min = df.min()
    df_normalized = (df - df_min) / (df_max - df_min)
    return df_normalized


"""""""""""""""
Trend
"""""""""""""""


def increasing_mavg(df, short_term, long_term, band_width):
    shorter_mavg = df['close'].to_frame().rolling(window=short_term).mean()
    longer_mavg = df['close'].to_frame().rolling(window=long_term).mean()
    longer_mavg_diff = longer_mavg.diff()
    ratio = shorter_mavg / longer_mavg
    mavg_buy = ratio[(ratio > (1 + band_width)) & (longer_mavg_diff > 0)]
    mavg_sell = ratio[(ratio < (1 - band_width))]
    mavg_buy = isnull_to_num(mavg_buy)
    mavg_sell = isnull_to_num(mavg_sell)
    return mavg_buy, mavg_sell


def bollinger_band(df, term, band_width):
    bband = df['close'].to_frame()
    mavg = df['close'].to_frame().rolling(window=term).mean()
    sigma = df['close'].to_frame().rolling(window=term).std()
    bband_upper = mavg + sigma * band_width
    bband_lower = mavg - sigma * band_width
    bband_buy = isnull_to_num(bband[bband < bband_lower])
    bband_sell = isnull_to_num(bband[bband > bband_upper])
    return bband_buy, bband_sell


def ma_convergence_divergence(df, short_term, long_term):
    ema_cp = df['close'].to_frame()
    ema_long = ema_cp.ewm(span=long_term).mean()
    ema_short = ema_cp.ewm(span=short_term).mean()
    macd = ema_short - ema_long
    macd_diff = macd.diff()
    macd_buy = isnull_to_num(macd[(macd > 0) & ((macd - macd_diff) < 0)])
    macd_sell = isnull_to_num(macd[(macd < 0) & ((macd - macd_diff) > 0)])
    return macd_buy, macd_sell


"""""""""""""""
Oscillator
"""""""""""""""


def ma_estrangement(df, term, band_width):
    mavg = df['close'].to_frame().rolling(window=term).mean()
    est_rate = df['close'].to_frame() / mavg
    est_buy = est_rate[est_rate > (1 + band_width)]
    est_sell = est_rate[est_rate < (1 - band_width)]
    est_buy = isnull_to_num(est_buy)
    est_sell = isnull_to_num(est_buy)
    return est_buy, est_sell


def commodity_channel_index(df, term, follower, contrarian):
    cci_cp = df['close'].to_frame()
    mavg = df['close'].to_frame().rolling(window=term).mean()
    price_std = df['close'].rolling(window=term).std()
    ccindex = (cci_cp - mavg) / (0.015 * price_std)
    cci_buy = isnull_to_num(cci_cp[((ccindex > 0) & (ccindex < follower)) | (ccindex < -contrarian)])
    cci_sell = isnull_to_num(cci_cp[((ccindex < 0) & (ccindex > -follower)) | (ccindex > contrarian)])
    return cci_buy, cci_sell


def relative_strength_index(df, term, follower, contrarian):
    rsi_cp = df['close'].to_frame()
    cp_diff = rsi_cp.diff()
    rsi_mother = np.fabs(cp_diff).rolling(window=term).sum()
    rsi_child = cp_diff.mask(cp_diff < 0, 0).rolling(window=term).sum()
    rsi = rsi_child / rsi_mother * 100
    rsi_buy = isnull_to_num(rsi[((rsi > 50) & (rsi < (50 + follower))) | (rsi < (50 - contrarian))])
    rsi_sell = isnull_to_num(rsi[((rsi < 50) & (rsi > (50 - follower))) | (rsi > (50 + contrarian))])
    return rsi_buy, rsi_sell

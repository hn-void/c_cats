def mavg(df, term, symbol='close'):
    df_mavg = df[symbol].copy().to_frame().rolling(window=term).mean().join(df['timestamp'])
    return df_mavg

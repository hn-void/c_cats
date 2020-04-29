import os
from unittest import TestCase

import pandas as pd

from c_cats.btc_utils import technical


class TestTechnicalIndicators(TestCase):

    def setUp(self):
        self.test_btc_df = pd.read_csv(os.path.dirname(__file__)+'/test_data/test_btc_historical.csv')

    def test_increasing_mavg(self):
        ima_buy, ima_sell = technical.increasing_mavg(self.test_btc_df, short_term=3, long_term=7, band_width=0.01)
        expected = pd.read_csv(os.path.dirname(__file__)+'/test_data/expected_data/cal_increasing_mavg.csv')
        expected_buy = expected['buy_signal'].fillna(0.0)
        expected_sell = expected['sell_signal'].fillna(0.0)
        self.assertTrue(ima_buy['close'].equals(expected_buy))
        self.assertTrue(ima_sell['close'].equals(expected_sell))

    def test_bollinger_band(self):
        bband_buy, bband_sell = technical.bollinger_band(self.test_btc_df, term=7, coefficient=1)
        expected = pd.read_csv(os.path.dirname(__file__)+'/test_data/expected_data/cal_bollinger_band.csv')
        expected_buy = expected['buy_signal'].fillna(0.0)
        expected_sell = expected['sell_signal'].fillna(0.0)
        self.assertTrue(bband_buy['close'].equals(expected_buy))
        self.assertTrue(bband_sell['close'].equals(expected_sell))

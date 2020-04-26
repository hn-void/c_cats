import os
from unittest import TestCase

from c_cats.btc_utils.handle_data import read_latest_btc


class TestReadLatestBTC(TestCase):

    def setUp(self):
        self.test_data = read_latest_btc(os.path.dirname(__file__)+'/test_data/test_btc_data.json', 'BTC')

    def test_read_latest_btc(self):
        self.assertEqual(self.test_data['id'], 1)
        self.assertEqual(self.test_data['quote']['JPY']['last_updated'], '2020-04-01')
        self.assertEqual(self.test_data['slug'], 'hoge')

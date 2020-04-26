import datetime

import pandas as pd

import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json


def is_latest(file_name):
    latest_date = pd.read_csv(file_name).tail(1)
    latest_date = latest_date.values.tolist()[0][8].split(' ')[0].replace('-', '')
    date_today = str(datetime.date.today()).replace('-', '')
    print('[c_cats] LAST_DATE: ' + latest_date)
    print('[c_cats] TODAY_DATE: ' + date_today)
    return int(latest_date) == int(date_today)


def get_historical_from_cryptocompare(
        symbol,
        comparison_symbol,
        limit=1,
        aggregate=1,
        exchange="Bitflyer",
        allData="true"):
    url = "https://min-api.cryptocompare.com/data/histoday?fsym={}&tsym={}&limit={}&aggregate={}&allData={}"\
        .format(symbol.upper(), comparison_symbol.upper(), limit, aggregate, allData)
    if exchange:
        url += "&e={}".format(exchange)
    page = requests.get(url)
    data = page.json()['Data']
    df = pd.DataFrame(data)
    df['timestamp'] = [datetime.datetime.fromtimestamp(d) for d in df.time]
    return df


# Using Free Tier
def get_price_from_coinmarketcap(file_name, api_key, url, convert, symbol):

    parameters = {
        'convert': convert,
        'symbol': symbol
    }

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key
    }

    session = requests.Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        with open(file_name, 'w') as output_file:
            json.dump(
                data,
                output_file,
                ensure_ascii=False,
                indent=4, sort_keys=True,
                separators=(',', ': '))
        print('[c_cats] Updated', file_name)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


def read_latest_btc(file_name, symbol):
    with open(file_name, 'r') as input_file:
        data = json.load(input_file)
        values = data['data']
        return values[symbol]

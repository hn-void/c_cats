from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json


def get_price_from_coinmarketcap(file_name, api_key, url, limit, convert):

    parameters = {
        'start': 1,
        'limit': limit,
        'convert': convert
    }

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key
    }

    session = Session()
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
        print('[c-cats]\tUpdated crypto_currency_data.json')
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


def read_latest_btc(file_name):
    with open(file_name, 'r') as input_file:
        data = json.load(input_file)
        values = data['data']
        return values[0]

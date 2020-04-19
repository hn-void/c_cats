import math

import handle_data
import mail


"""""""""""""""
Edit here ↓
"""""""""""""""
FILE_NAME = 'crypto_currency_data.json'
API_KEY = 'YOUR_COINMARKETCAP_API_KEY'
URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
LIMIT = 100
CONVERT = 'JPY'

FROM_ADDR = 'YOUR_EMAIL'
FROM_ADDR_PASSWORD = 'PASSWORD'
TO_ADDRS = ['TO_ADDR1', 'TO_ADDR2', '...']
SUBJECT = 'c( ◠∞◠ c)<Bitcoin週間レポートです'

THRESHOLD_UPPER = 800000
THRESHOLD_LOWER = 600000
THRESHOLD_PERCENTAGE_1h = 5
"""""""""""""""
Edit here ↑
"""""""""""""""

print('[c-cats]\tWelcome to c-cats simple mail service')

handle_data.get_price_from_coinmarketcap(
    file_name=FILE_NAME,
    api_key=API_KEY,
    url=URL,
    limit=LIMIT,
    convert=CONVERT)
latest_btc = handle_data.read_latest_btc(file_name=FILE_NAME)

current_price = latest_btc['quote'][CONVERT]['price']
percent_change_1h = latest_btc['quote'][CONVERT]['percent_change_1h']
last_updated = latest_btc['quote'][CONVERT]['last_updated']

mail_flag = 0
body = last_updated + '\n'
body += str(current_price) + 'JPY/BTC\n'
if current_price > THRESHOLD_UPPER:
    body += 'c( ◠∞◠ c)<Bitcoinが 800000 JPY/BTC を上回りました．\n'
    mail_flag = 1
elif current_price < THRESHOLD_LOWER:
    body += 'c( ◠∞◠ c)<Bitcoinが 600000 JPY/BTC を下回りました．\n'
    mail_flag = 1
if math.fabs(percent_change_1h) > THRESHOLD_PERCENTAGE_1h:
    body += 'c( ◠∞◠ c)<Bitcoinの値段が大きく変動しています(' + percent_change_1h + '%)．\n'
    mail_flag = 1

if mail_flag == 1:
    for to_addr in TO_ADDRS:
        msg = mail.create_mail(FROM_ADDR, to_addr, SUBJECT, body)
        mail.send_mail(FROM_ADDR, FROM_ADDR_PASSWORD, to_addr, msg)
    print('[c-cats]\tSent emails')
else:
    print('[c-cats]\tNot send emails')

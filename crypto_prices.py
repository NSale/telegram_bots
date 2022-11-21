import json, requests, os, logging
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

# coinmarketcap constants
FIAT = 'EUR'
CURRENCIES = ['Bitcoin', 'Ethereum', 'XRP', 'Cardano',  'Polkadot', 'Solana', 'Polygon']
URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
PARAMETERS = {
  'start':'1',
  'limit':'25',
  'convert': FIAT
}
try: 
  API_KEY_COINMARKETCAP = os.environ['API_KEY_COINMARKETCAP']
except KeyError:
  logging.error('API key for coinmarketcap is not available!')
HEADERS = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': API_KEY_COINMARKETCAP,
}
session = Session()
session.headers.update(HEADERS)

# telegram constants
try: 
  API_TOKEN = os.environ['API_TOKEN']
except KeyError:
  logging.error('API token for telegram is not available!')
try: 
  CHAT_ID = os.environ['CHAT_ID']
except KeyError:
  logging.error('Chat id for telegram is not available!')
API_URL = f'https://api.telegram.org/bot{API_TOKEN}/sendMessage'

data = []
prices = {}

try:
  response = session.get(URL, params=PARAMETERS)
  data = json.loads(response.text)
  data = data['data']
except (ConnectionError, Timeout, TooManyRedirects) as e:
  logging.error(e)

for currency in data:
  if currency['name'] in CURRENCIES:
    currency_name = currency['name']
    prices[currency_name] = [
        round(currency['quote'][FIAT]['price'], 2), 
        round(currency['quote'][FIAT]['percent_change_24h'], 2)
    ]

def make_message():
    message = ''
    for key, value in prices.items():
        message += key + ' price: ' + str(value[0]) + ' EUR, 24h_change: ' + str(value[1]) + '%' + '\n'
    return message

def send_to_telegram():
    try:
        requests.post(API_URL, json={'chat_id': CHAT_ID, 'text': make_message()})
    except Exception as e:
        logging.error(e)

send_to_telegram()
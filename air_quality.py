import json, requests, os, logging
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

# AirVisual constants
try: 
  API_KEY_AIRVISUAL = os.environ['API_KEY_AIRVISUAL']
except KeyError:
  logging.error('API token for airVisuel is not available!')
COUNTRY = 'Serbia'
STATE = 'Autonomna Pokrajina Vojvodina'
CITY = 'Novi Sad'
URL = f'http://api.airvisual.com/v2/city?city={CITY}&state={STATE}&country={COUNTRY}&key={API_KEY_AIRVISUAL}'

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

session = Session()
data = {}

try:
  response = session.get(URL)
  data = json.loads(response.text)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  logging.error(e)

pollution = data['data']['current']['pollution']

def get_air_quality(polution_degree):
  if polution_degree in range(0,51):
    return 'добар'
  elif polution_degree in range(51,101):
    return 'умерено загађен'
  elif polution_degree in range(101,151):
    return 'нездрав за осетљиве групе'
  elif polution_degree in range(151,201):
    return 'нездрав'
  elif polution_degree in range(201,301):
    return 'веома нездрав'
  else:
    return 'опасан'

def get_polutant(unit):
  if unit == 'p2':
    return 'су PM2.5 честице'
  elif unit == 'p1':
    return 'су PM10 честице'
  elif unit == 'o3':
    return 'је O3 озон'
  elif unit == 'n2':
    return 'је NO2 азот-диоксид'
  elif unit == 's2':
    return 'је SO2 сумпор-диоксид'
  elif unit == 'co':
    return 'је CO угљен-диоксид'
  else: 
    return 'је непознат загађивач'

def make_message():
    return f"Загађење је US AQI {pollution['aqius']}, ваздух је {get_air_quality(pollution['aqius'])}, а главни загађивач {get_polutant(pollution['mainus'])}."

def send_to_telegram():
    try:
        requests.post(API_URL, json={'chat_id': CHAT_ID, 'text': make_message()})
    except Exception as e:
        logging.error(e)

send_to_telegram()
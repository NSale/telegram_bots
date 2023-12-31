import json, requests, os, logging
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

# openweathermap constants
try: 
  API_KEY_OPENWEATHERMAP = os.environ['API_KEY_OPENWEATHERMAP']
except KeyError:
  logging.error('API token for openweathermap is not available!')
LAT = 45.2396085
LON = 19.8227056 
URL = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={LAT}&lon={LON}&appid={API_KEY_OPENWEATHERMAP}'

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

polution_degre = data['list'][0]['main']['aqi']

def get_air_quality(polution_degree):
  if polution_degree in range(1):
    return 'добар'
  elif polution_degree in range(2):
    return 'умерено загађен'
  elif polution_degree in range(3):
    return 'нездрав за осетљиве групе'
  elif polution_degree in range(4):
    return 'нездрав'
  else:
    return 'веома нездрав'

polutants = data['list'][0]['components']
  

def make_message():
    return f"Индекс загађења је  {polution_degre}, ваздух је {get_air_quality(polution_degre)}, а загађивачи су следећи: {polutants}."

def send_to_telegram():
    try:
        requests.post(API_URL, json={'chat_id': CHAT_ID, 'text': make_message()})
    except Exception as e:
        logging.error(e)

send_to_telegram()
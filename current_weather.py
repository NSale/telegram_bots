import json, requests, os, logging
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

# openweathermap constants
try: 
#   API_KEY_OPENWEATHERMAP = os.environ['API_KEY_OPENWEATHERMAP']
  API_KEY_OPENWEATHERMAP = '92ec0d7ac0eb6f819f3cbb4878cf822d'
except KeyError:
  logging.error('API token for openweathermap is not available!')
LAT = 45.2396085
LON = 19.8227056 
URL = f'http://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&units=metric&appid={API_KEY_OPENWEATHERMAP}'

# telegram constants
try: 
#   API_TOKEN = os.environ['API_TOKEN']
   API_TOKEN = '5668465982:AAERJNaPbyjL9mpsXpXGiUWp3ohV-cDtKFE'
except KeyError:
  logging.error('API token for telegram is not available!')
try: 
#   CHAT_ID = os.environ['CHAT_ID']
   CHAT_ID = '1631600460'
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
weather_data = data['main']

def make_message():
    return f"Тренутна температура је {str(weather_data['temp'])}\N{DEGREE SIGN}C, субјективни осећај је {str(weather_data['feels_like'])}\N{DEGREE SIGN}C. Ваздушни притисак је {str(weather_data['pressure'])} mbar, влажност ваздуха {str(weather_data['humidity'])}%, а брзина ветра {str(data['wind']['speed'])} m/s."

def send_to_telegram():
    try:
        requests.post(API_URL, json={'chat_id': CHAT_ID, 'text': make_message()})
    except Exception as e:
        logging.error(e)

send_to_telegram()
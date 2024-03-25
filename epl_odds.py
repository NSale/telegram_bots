import json, requests, os, logging
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

# the-odds-api constants
try: 
  API_KEY = os.environ['API_KEY_THE_ODDS_API']
except KeyError:
  logging.error('API token for the-odds-api is not available!')
SPORT = 'soccer_epl'
REGION = 'uk' 
URL = f'https://api.the-odds-api.com//v4/sports/{SPORT}/odds/?apiKey={API_KEY}&regions={REGION}'

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
  first_gw = data[:10]
  second_gw = data[10:20]
  third_gw = data[20:]
except (ConnectionError, Timeout, TooManyRedirects) as e:
  logging.error(e)

team_odds_first_gw = {}
team_odds_second_gw = {}
team_odds_third_gw = {}

for event in first_gw:
    team_one_name = event['bookmakers'][0]['markets'][0]['outcomes'][0]['name']
    team_two_name = event['bookmakers'][0]['markets'][0]['outcomes'][1]['name']
    team_one_odds = event['bookmakers'][0]['markets'][0]['outcomes'][0]['price']
    team_two_odds = event['bookmakers'][0]['markets'][0]['outcomes'][1]['price']
    team_odds_first_gw.update({team_one_name: team_one_odds})
    team_odds_first_gw.update({team_two_name: team_two_odds})

for event in second_gw:
    team_one_name = event['bookmakers'][0]['markets'][0]['outcomes'][0]['name']
    team_two_name = event['bookmakers'][0]['markets'][0]['outcomes'][1]['name']
    team_one_odds = event['bookmakers'][0]['markets'][0]['outcomes'][0]['price']
    team_two_odds = event['bookmakers'][0]['markets'][0]['outcomes'][1]['price']
    team_odds_second_gw.update({team_one_name: team_one_odds})
    team_odds_second_gw.update({team_two_name: team_two_odds})

for event in third_gw:
    team_one_name = event['bookmakers'][0]['markets'][0]['outcomes'][0]['name']
    team_two_name = event['bookmakers'][0]['markets'][0]['outcomes'][1]['name']
    team_one_odds = event['bookmakers'][0]['markets'][0]['outcomes'][0]['price']
    team_two_odds = event['bookmakers'][0]['markets'][0]['outcomes'][1]['price']
    team_odds_third_gw.update({team_one_name: team_one_odds})
    team_odds_third_gw.update({team_two_name: team_two_odds})

best_five_odss_gw1 = sorted(team_odds_first_gw.items(), key=lambda item: item[1])[:5]
best_five_odss_gw2 = sorted(team_odds_second_gw.items(), key=lambda item: item[1])[:5]
best_five_odss_gw3 = sorted(team_odds_third_gw.items(), key=lambda item: item[1])[:5]

  

def make_message():
    return f"Best odds for the next gw: {best_five_odss_gw1}, gw after that: {best_five_odss_gw2} and the last gw: {best_five_odss_gw3}."

def send_to_telegram():
    try:
        requests.post(API_URL, json={'chat_id': CHAT_ID, 'text': make_message()})
    except Exception as e:
        logging.error(e)

send_to_telegram()
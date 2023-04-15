import os
import json

# Config path
CONFIG_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../config.json')

# Required config properties
REQUIRED = [
  'LATITUDE',
  'LONGITUDE',
  'WEATHER_KEY',
  'BTC_AMOUNT',
  'ETH_AMOUNT',
  'CRYPTO_DISPLAY_MODE',
  'NEWS_CATEGORY',
  'TWITTER_SCREEN_NAME',
  'TWITTER_BEARER_TOKEN',
  'SPOTIFY_CLIENT_ID',
  'SPOTIFY_CLIENT_SECRET',
  'SPOTIFY_REDIRECT_URI'
]

config = {}

#
# Validate config has all expected properties
def validate():
  for prop in REQUIRED:
    if not prop in config:
      raise Exception(f'Config requires {prop}')

#
# Read local config.json file
#
def load():
  global config

  with open(CONFIG_PATH, 'r') as file:
    config = json.loads(file.read())

  validate()

  print(f"[config] {config}")

#
# Get a config value
#
def get(key):
  return config[key]

import os
import json
from modules import log

# Config path
CONFIG_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../config.json')

#
# Read local config.json file
#
def load():
  global config

  with open(CONFIG_PATH, 'r') as file:
    config = json.loads(file.read())

  log.info('config', config)

load()

#
# Require a config key
# 
def require(keys):
  for key in keys:
    if key not in config:
      raise Exception(f'Missing config: {key}')

#
# Get a config value
#
def get(key):
  return config[key]

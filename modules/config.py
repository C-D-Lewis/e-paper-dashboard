import os
import json

CONFIG_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../config.json')

config = {}

# Read local config.json file
def load():
  global config

  with open(CONFIG_PATH, 'r') as file:
    config = json.loads(file.read())
  print(f"config: {config}")

# Get a config value
def get(name):
  return config[name]

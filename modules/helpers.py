import os
import json
from datetime import datetime

CONFIG_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../config.json')

config = {}

# Read local config.json file
def load_config():
  global config

  with open(CONFIG_PATH, 'r') as file:
    config = json.loads(file.read())
  print(config)

# Wrap text based on line length
# Adapted from https://itnext.io/how-to-wrap-text-on-image-using-python-8f569860f89e
def get_wrapped_lines(text, font, max_width):
  lines = []

  words = text.split(' ')
  i = 0
  while i < len(words):
    line = ''
    while i < len(words) and font.getsize(line + words[i])[0] <= max_width:
      line = line + words[i]+ " "
      i += 1
    if not line:
      line = words[i]
      i += 1
    lines.append(line)
  return lines

import platform, sys, os, time
import urllib.request, json
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

CONFIG_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.json')

# Fonts
FONTS_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts')
FONT_28 = ImageFont.truetype(os.path.join(FONTS_DIR, 'KeepCalm-Medium.ttf'), 28)
FONT_48 = ImageFont.truetype(os.path.join(FONTS_DIR, 'KeepCalm-Medium.ttf'), 48)
FONT_80 = ImageFont.truetype(os.path.join(FONTS_DIR, 'KeepCalm-Medium.ttf'), 80)

# Images
IMAGES_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'images')
ICON_CLOUD = Image.open(os.path.join(IMAGES_DIR, 'cloud.bmp'))
ICON_WIND = Image.open(os.path.join(IMAGES_DIR, 'wind.bmp'))
ICON_RAIN = Image.open(os.path.join(IMAGES_DIR, 'rain.bmp'))
ICON_SUN = Image.open(os.path.join(IMAGES_DIR, 'sun.bmp'))
ICON_MOON = Image.open(os.path.join(IMAGES_DIR, 'moon.bmp'))
ICON_STORM = Image.open(os.path.join(IMAGES_DIR, 'storm.bmp'))
ICON_SNOW = Image.open(os.path.join(IMAGES_DIR, 'snow.bmp'))
ICON_FROST = Image.open(os.path.join(IMAGES_DIR, 'frost.bmp'))
ICON_FOG = Image.open(os.path.join(IMAGES_DIR, 'fog.bmp'))
ICON_TFL = Image.open(os.path.join(IMAGES_DIR, 'tfl.bmp'))
ICON_GA = Image.open(os.path.join(IMAGES_DIR, 'ga.bmp'))
ICON_BTC = Image.open(os.path.join(IMAGES_DIR, 'btc.bmp'))
ICON_ETH = Image.open(os.path.join(IMAGES_DIR, 'eth.bmp'))
ICON_ERROR = Image.open(os.path.join(IMAGES_DIR, 'error.bmp'))
ICON_QUESTION_MARK = Image.open(os.path.join(IMAGES_DIR, 'question.bmp'))

# Constants
WEATHER_UPDATE_S = 1000 * 60 * 15
RAIL_URL = 'http://www.nationalrail.co.uk/service_disruptions/indicator.aspx'
RAIL_UPDATE_S = 1000 * 60 * 10
DAY_START_HOUR = 6
DAY_END_HOUR = 18
CRYPTO_UPDATE_S = 1000 * 60 * 10

config = {}

weather_data = {
  'last_update': 0,
  'current_temp': 0,
  'current_summary': 'unknown',
  'current_icon': 'unknown',
  'temp_high': 0,
  'temp_low': 0
}

rail_data = {
  'last_update': 0
}

crypto_data = {
  'last_update': 0,
  'BTC': {
    'value': 0,
    'change': 0,
  },
  'ETH': {
    'value': 0,
    'change': 0
  }
}

# Only runs on Pi
if 'arm' not in platform.machine():
  print('Not ARM, quitting')
  sys.exit(0)

from lib.waveshare_epd import epd7in5_V2

epd = epd7in5_V2.EPD()
width = epd.width
height = epd.height

################################### Helpers ####################################

# Read local config.json file
def load_config():
  global config

  with open(CONFIG_PATH, 'r') as file:
    config = json.loads(file.read())
  print(config)

# Get an appropriate weather icon
def get_weather_icon():
  current_icon = weather_data['current_icon'].lower()
  now = datetime.now()
  hours = now.hour

  if 'cloud' in current_icon or 'overcast' in current_icon:
    return ICON_CLOUD
  if 'wind' in current_icon:
    return ICON_WIND
  if 'rain' in current_icon:
    return ICON_RAIN
  if 'clear' in current_icon or 'sun' in current_icon:
    if hours > DAY_START_HOUR and hours < DAY_END_HOUR:
      return ICON_SUN
    else:
      return ICON_MOON
  if 'thunder' in current_icon or 'storm' in current_icon or 'lighting' in current_icon:
    return ICON_STORM
  if 'snow' in current_icon:
    return ICON_SNOW
  if 'ice' in current_icon or 'frost' in current_icon:
    return ICON_FROST
  if 'mist' in current_icon or 'fog' in current_icon or 'haz' in current_icon:
    return ICON_FOG

  if 'error' in current_icon:
    return ICON_ERROR
  return ICON_QUESTION_MARK  

#################################### Network ###################################

# Get a page body
def fetch_text(url):
  with urllib.request.urlopen(url) as req:
    return req.read().decode()

# Get some JSON
def fetch_json(url):
  return json.loads(fetch_text(url))

# Update weather data
def update_weather_data():
  global weather_data

  try:
    url = f"https://api.darksky.net/forecast/{config['DARKSKY_KEY']}/{config['LATITUDE']},{config['LONGITUDE']}?units=auto&exclude=hourly,minutely"
    new_data = fetch_json(url)
    weather_data['current_temp'] = round(new_data['currently']['apparentTemperature'])
    weather_data['current_summary'] = new_data['currently']['summary']
    weather_data['current_icon'] = new_data['currently']['icon']
    weather_data['temp_high'] = round(new_data['daily']['data'][0]['apparentTemperatureHigh'])
    weather_data['temp_low'] = round(new_data['daily']['data'][0]['apparentTemperatureLow'])
    print(weather_data)
  except Exception as err:
    print("update_weather_data error: {0}".format(err))
    weather_data['current_temp'] = '!'
    weather_data['current_summary'] = 'error'
    weather_data['current_icon'] = 'error'
    weather_data['temp_high'] = '!'
    weather_data['temp_low'] = '!'

# Fetch rail operator status
def fetch_operator_status(operator_name):
  body = fetch_text(RAIL_URL)
  start = body.index(f"{operator_name}</td>")
  temp = body[start:]
  start = temp.index('<td>') + 4
  temp = temp[start:]
  end = temp.index('</td>')
  return temp[:end]

# Fetch rail network delays status
def update_rail_data():
  try:
    rail_data['TfL Rail'] = fetch_operator_status('TfL Rail')
    rail_data['Greater Anglia'] = fetch_operator_status('Greater Anglia')
    print(rail_data)
  except Exception as err:
    print("update_rail_data error: {0}".format(err))
    rail_data['TfL Rail'] = 'error'
    rail_data['Greater Anglia'] = 'error'

# Update crypto portfolio
def update_crypto_data():
  try:
    url = f"https://api.nomics.com/v1/currencies/ticker?key={config['NOMICS_KEY']}&ids=BTC,ETH&interval=1d,30d&convert=GBP"
    res = fetch_json(url)
    
    crypto_data['BTC']['value'] = round(config['BTC_AMOUNT'] * float(res[0]['price']), 2)
    crypto_data['BTC']['change'] = round(float(res[0]['1d']['price_change']), 2)
    crypto_data['ETH']['value'] = round(config['ETH_AMOUNT'] * float(res[1]['price']), 2)
    crypto_data['ETH']['change'] = round(float(res[1]['1d']['price_change']), 2)
    print(crypto_data)
  except Exception as err:
    print("update_crypto_data error: {0}".format(err))
    crypto_data['BTC']['value'] = 0
    crypto_data['BTC']['change'] = 0
    crypto_data['ETH']['value'] = 0
    crypto_data['ETH']['change'] = 0

################################# Draw modules #################################

# Draw time module
def draw_date_and_time(canvas):
  now = datetime.now()
  time_str = now.strftime("%H:%M")
  canvas.text((10, 10), time_str, font = FONT_80, fill = 0)
  date_str = now.strftime("%B %d, %Y")
  canvas.text((10, 95), date_str, font = FONT_48, fill = 0)

# Draw a divider
def draw_divider(canvas, x, y, w, h):
  canvas.rectangle([x, y, x + w, y + h], fill = 0)

# Draw the weather icon, temperature, and conditions
def draw_weather(canvas, image):
  image.paste(get_weather_icon(), (520, 10))
  temp_str = f"{weather_data['current_temp']}°C"
  canvas.text((660, 30), temp_str, font = FONT_48, fill = 0)
  temp_high_low_str = f"{weather_data['temp_high']} | {weather_data['temp_low']}"
  canvas.text((660, 85), temp_high_low_str, font = FONT_28, fill = 0)

# Draw rail statuses
def draw_rail_status(canvas, image):
  image.paste(ICON_TFL, (15, 175))
  str = f"{rail_data['TfL Rail']}"
  canvas.text((95, 191), str, font = FONT_28, fill = 0)

  image.paste(ICON_GA, (15, 239))
  str = f"{rail_data['Greater Anglia']}"
  canvas.text((95, 255), str, font = FONT_28, fill = 0)

# Draw crypto values
def draw_crypto_values(canvas, image):
  image.paste(ICON_BTC, (15, 335))
  arrow = '+' if crypto_data['BTC']['change'] > 0 else '-'
  value_str = f"£{crypto_data['BTC']['value']}"
  change_str = f"{arrow} £{crypto_data['BTC']['change']}"
  canvas.text((95, 338), value_str, font = FONT_28, fill = 0)
  canvas.text((95, 374), change_str, font = FONT_28, fill = 0)

  image.paste(ICON_ETH, (15, 409))
  arrow = '+' if crypto_data['ETH']['change'] > 0 else '-'
  value_str = f"£{crypto_data['ETH']['value']}"
  change_str = f"{arrow} £{crypto_data['ETH']['change']}"
  canvas.text((95, 412), value_str, font = FONT_28, fill = 0)
  canvas.text((95, 448), change_str, font = FONT_28, fill = 0)

################################## Main loop ###################################

# Draw things
def draw():
  # Prepare
  image = Image.new('1', (width, height), 255)  # Mode = 1bit
  canvas = ImageDraw.Draw(image)
  canvas.rectangle((0, 0, width, height), fill = 255)

  # Draw content
  draw_date_and_time(canvas)
  draw_divider(canvas, 14, 155, width - 28, 5)
  draw_weather(canvas, image)
  draw_rail_status(canvas, image)
  draw_divider(canvas, 14, 310, 300, 5)
  draw_crypto_values(canvas, image)
  draw_divider(canvas, 350, 175, 5, 300)
  
  # Update display
  epd.display(epd.getbuffer(image))
  time.sleep(2)

# Update all the things
def update():
  now = time.time()

  if now - weather_data['last_update'] > WEATHER_UPDATE_S:
    update_weather_data()
    weather_data['last_update'] = now

  if now - rail_data['last_update'] > RAIL_UPDATE_S:
    update_rail_data()
    rail_data['last_update'] = now

  if now - crypto_data['last_update'] > CRYPTO_UPDATE_S:
    update_crypto_data()
    crypto_data['last_update'] = now

# The main function
def main():
  load_config()
  epd.init()
  print('Ready')

  # Update once a minute
  while True:
    update()
    draw()
    epd.sleep()
    time.sleep(58)
    epd.init()

if __name__ in '__main__':
  try:
    main()
  except KeyboardInterrupt:    
    print('Exiting')
    epd7in5_V2.epdconfig.module_exit()
    exit()

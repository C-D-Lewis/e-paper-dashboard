import platform, sys, os, time
import urllib.request, json
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

# Read env
DARKSKY_KEY = os.environ.get('DARKSKY_KEY')
LATITUDE = os.environ.get('LATITUDE')
LONGITUDE = os.environ.get('LONGITUDE')

FONT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'font')
FONT_48 = ImageFont.truetype(os.path.join(FONT_DIR, 'KeepCalm-Medium.ttf'), 48)
FONT_80 = ImageFont.truetype(os.path.join(FONT_DIR, 'KeepCalm-Medium.ttf'), 80)
WEATHER_URL = f"https://api.darksky.net/forecast/{DARKSKY_KEY}/{LATITUDE},{LONGITUDE}?units=auto&exclude=hourly"
WEATHER_UPDATE_S = 1000 * 60 * 15

weather_data = {
  'last_update': 0,
  'current_temp': 0,
  'current_conditions': 'unknown',
}

# Only runs on Pi
if 'arm' not in platform.machine():
  print('Not ARM, quitting')
  sys.exit(0)

from lib.waveshare_epd import epd7in5_V2

epd = epd7in5_V2.EPD()
width = epd.width
height = epd.height

# Get some JSON
def get_json(url):
  with urllib.request.urlopen(url) as req:
    data = json.loads(req.read().decode())
    return data

# Draw time module
def draw_date_and_time(image_draw):
  now = datetime.now()
  time_str = now.strftime("%H:%M")
  image_draw.text((10, 10), time_str, font = FONT_80, fill = 0)
  date_str = now.strftime("%B %d, %Y")
  image_draw.text((10, 95), date_str, font = FONT_48, fill = 0)

# Draw a divider
def draw_divider(image_draw, x, y, w, h):
  image_draw.rectangle([x, y, x + w, y + h], fill = 0)

# Draw things
def draw():
  # Prepare
  image = Image.new('1', (width, height), 255)  # Mode = 1bit
  image_draw = ImageDraw.Draw(image)
  image_draw.rectangle((0, 0, width, height), fill = 255)

  # Draw content
  draw_date_and_time(image_draw)
  draw_divider(image_draw, 14, 155, width - 28, 5)
  
  # Update display
  epd.display(epd.getbuffer(image))
  time.sleep(2)

# Update weather data
def update_weather_data():
  new_data = get_json(WEATHER_URL)
  print(new_data)

# Update all the things
def update():
  now = time.time()
  if now - weather_data['last_update'] > WEATHER_UPDATE_S:
    update_weather_data()

# The main function
def main():
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

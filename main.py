import platform, sys, os, time
import urllib.request, json
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

# Read env
DARKSKY_KEY = os.environ.get('DARKSKY_KEY')
LATITUDE = os.environ.get('LATITUDE')
LONGITUDE = os.environ.get('LONGITUDE')

FONTS_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts')
FONT_28 = ImageFont.truetype(os.path.join(FONTS_DIR, 'KeepCalm-Medium.ttf'), 28)
FONT_48 = ImageFont.truetype(os.path.join(FONTS_DIR, 'KeepCalm-Medium.ttf'), 48)
FONT_80 = ImageFont.truetype(os.path.join(FONTS_DIR, 'KeepCalm-Medium.ttf'), 80)

IMAGES_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'images')
ICON_CLOUD = Image.open(os.path.join(IMAGES_DIR, 'cloud.bmp'))

WEATHER_URL = f"https://api.darksky.net/forecast/{DARKSKY_KEY}/{LATITUDE},{LONGITUDE}?units=auto&exclude=hourly,minutely"
WEATHER_UPDATE_S = 1000 * 60 * 15

weather_data = {
  'last_update': 0,
  'current_temp': 0,
  'current_summary': 'unknown',
  'current_icon': 'unknown'
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
  image.paste(ICON_CLOUD, (530, 10))
  weather_str = f"{weather_data['current_temp']}°C"
  canvas.text((660, 50), weather_str, font = FONT_48, fill = 0)

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
  
  # Update display
  epd.display(epd.getbuffer(image))
  time.sleep(2)

# Update weather data
def update_weather_data():
  new_data = get_json(WEATHER_URL)
  weather_data['current_temp'] = round(new_data['currently']['apparentTemperature'])
  weather_data['current_summary'] = new_data['currently']['summary']
  weather_data['current_icon'] = new_data['currently']['icon']
  print(weather_data)

# Update all the things
def update():
  now = time.time()

  if now - weather_data['last_update'] > WEATHER_UPDATE_S:
    update_weather_data()
    weather_data['last_update'] = now

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

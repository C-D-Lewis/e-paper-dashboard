import platform, sys, os, time
import urllib.request, json
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

# Read env
DARKSKY_KEY = os.environ.get('DARKSKY_KEY')
LATITUDE = os.environ.get('LATITUDE')
LONGITUDE = os.environ.get('LONGITUDE')

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
ICON_QUESTION_MARK = Image.open(os.path.join(IMAGES_DIR, 'question.bmp'))

# Constants
WEATHER_URL = f"https://api.darksky.net/forecast/{DARKSKY_KEY}/{LATITUDE},{LONGITUDE}?units=auto&exclude=hourly,minutely"
WEATHER_UPDATE_S = 1000 * 60 * 15
DAY_START_HOUR = 6
DAY_END_HOUR = 18

weather_data = {
  'last_update': 0,
  'current_temp': 0,
  'current_summary': 'unknown',
  'current_icon': 'unknown',
  'temp_high': 0,
  'temp_low': 0
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

# Get an appropriate weather icon
def get_weather_icon():
  summary_lower = weather_data['current_summary'].lower()
  now = datetime.now()
  hours = now.hour

  if 'cloud' in summary_lower or 'overcast' in summary_lower:
    return ICON_CLOUD
  if 'wind' in summary_lower:
    return ICON_WIND
  if 'rain' in summary_lower:
    return ICON_RAIN
  if 'clear' in summary_lower or 'sun' in summary_lower:
    if hours > DAY_START_HOUR and hours < DAY_END_HOUR:
      return ICON_SUN
    else:
      return ICON_MOON
  if 'thunder' in summary_lower or 'storm' in summary_lower or 'lighting' in summary_lower:
    return ICON_STORM
  if 'snow' in summary_lower:
    return ICON_SNOW
  # ice
  # mist | fog

  return ICON_QUESTION_MARK

#################################### Network ###################################

# Get some JSON
def get_json(url):
  with urllib.request.urlopen(url) as req:
    data = json.loads(req.read().decode())
    return data

# Update weather data
def update_weather_data():
  new_data = get_json(WEATHER_URL)
  weather_data['current_temp'] = round(new_data['currently']['apparentTemperature'])
  weather_data['current_summary'] = new_data['currently']['summary']
  weather_data['current_icon'] = new_data['currently']['icon']
  weather_data['temp_high'] = round(new_data['daily']['data'][0]['apparentTemperatureHigh'])
  weather_data['temp_low'] = round(new_data['daily']['data'][0]['apparentTemperatureLow'])
  print(weather_data)

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
  
  # Update display
  epd.display(epd.getbuffer(image))
  time.sleep(2)

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

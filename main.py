import platform, sys, os, time
import json
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

from modules import fetch, helpers, fonts, weather, images, rail, news, crypto

RUNNING_ON_PI = 'arm' in platform.machine()
print({ 'RUNNING_ON_PI': RUNNING_ON_PI })

# Constants
UPDATE_INTERVAL_M = 15

# Only runs on Pi
if RUNNING_ON_PI:
  from lib.waveshare_epd import epd7in5_V2
  epd = epd7in5_V2.EPD()
  width = epd.width
  height = epd.height
else:
  print('[TEST] EPD import')
  width = 800
  height = 480

################################## Testability #################################

# Initialise the display
def init_display():
  if RUNNING_ON_PI:
    epd.init()
  else:
    print('[TEST] epd.init()')

# Handle updating the display
def update_display(image):
  if RUNNING_ON_PI:
    epd.display(epd.getbuffer(image))
  else:
    print('[TEST] epd.display()')

# Handle sleeping the display
def sleep_display():
  if RUNNING_ON_PI:
    epd.sleep()
  else:
    print('[TEST] epd.sleep()')

# Handle deinitialising the display
def deinit_display():
  if RUNNING_ON_PI:
    epd7in5_V2.epdconfig.module_exit()
  else:
    print('SKipping module_exit()')

################################### Drawing ####################################

# Draw time module
def draw_date_and_time(canvas):
  now = datetime.now()
  time_str = now.strftime("%H:%M")
  canvas.text((10, 10), time_str, font = fonts.KEEP_CALM_80, fill = 0)
  date_str = now.strftime("%B %d, %Y")
  canvas.text((10, 95), date_str, font = fonts.KEEP_CALM_48, fill = 0)

# Draw a divider
def draw_divider(canvas, x, y, w, h):
  canvas.rectangle([x, y, x + w, y + h], fill = 0)

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
  weather.draw(canvas, image)
  rail.draw(canvas, image)
  draw_divider(canvas, 14, 310, 310, 5)
  crypto.draw(canvas, image)
  draw_divider(canvas, 350, 185, 5, 280)
  news.draw(canvas, image)

  # Update display
  update_display(image)
  time.sleep(2)

# Update all data sources
def update_data_sources():
  weather.update_data()
  rail.update_data()
  crypto.update_data()
  news.update_data()

# Update all the things
def update():
  now = datetime.now()
  if now.minute % UPDATE_INTERVAL_M == 0:
    update_data_sources()

# The main function
def main():
  helpers.load_config()
  init_display()

  # Initial data download
  update_data_sources()

  # Update once a minute
  while True:
    update()
    draw()
    sleep_display()
    time.sleep(58)
    init_display()

if __name__ in '__main__':
  try:
    main()
  except KeyboardInterrupt:
    print('Exiting')
    deinit_display()
    exit()

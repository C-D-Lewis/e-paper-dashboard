import platform, sys, os, time
import json
from PIL import Image, ImageDraw
from datetime import datetime

from modules import fetch, fonts, images, config
from widgets import weather, rail, news, crypto

RUNNING_ON_PI = 'arm' in platform.machine()
print({ 'RUNNING_ON_PI': RUNNING_ON_PI })

# Constants
UPDATE_INTERVAL_M = 15
NUM_PAGES = 2

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
    image.save('render.png')

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
    print('[TEST] module_exit()')

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

# Draw cycling page indicators
def draw_page_indicators(canvas, page_index):
  root_x = 365
  root_y = 300
  gap_y = 25
  size = 8

  for index in range(0, NUM_PAGES):
    selected = page_index == index
    fill = 0 if selected else 1
    canvas.ellipse((root_x - 2, root_y - 2, root_x + size + 2, root_y + size + 2), fill = 0)
    canvas.ellipse((root_x, root_y, root_x + size, root_y + size), fill = fill)
    
    root_y += gap_y

################################## Main loop ###################################

# Draw things
def draw():
  # Prepare
  image = Image.new('1', (width, height), 255)  # Mode = 1bit
  canvas = ImageDraw.Draw(image)
  canvas.rectangle((0, 0, width, height), fill = 255)

  # Draw content
  draw_date_and_time(canvas)
  draw_divider(canvas, 14, 160, width - 28, 5)
  weather.draw(canvas, image)
  rail.draw(canvas, image)
  draw_divider(canvas, 14, 310, 310, 5)
  crypto.draw(canvas, image)
  draw_divider(canvas, 350, 185, 5, 280)

  # Cycling pages
  now = datetime.now()
  page_index = now.minute % NUM_PAGES
  if page_index == 0:
    news.draw(canvas, image)
  elif page_index == 1:
    weather.draw_forecast(canvas, image)
  else:
    print(f"! Unused page_index {page_index}")
  draw_page_indicators(canvas, page_index)

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

# Wait for the next minute
def wait_for_next_minute():
  now = datetime.now()
  while now.second != 0:
    now = datetime.now()
    time.sleep(1)

# The main function
def main():
  config.load()
  update_data_sources()

  # Update once a minute
  while True:
    update()
    init_display()
    draw()
    sleep_display()
    wait_for_next_minute()

if __name__ in '__main__':
  try:
    main()
  except KeyboardInterrupt:
    print('Exiting')
    deinit_display()
    exit()

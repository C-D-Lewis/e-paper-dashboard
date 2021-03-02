import platform
import sys
import os
import time
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

fontdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'font')

font_48 = ImageFont.truetype(os.path.join(fontdir, 'KeepCalm-Medium.ttf'), 48)
font_80 = ImageFont.truetype(os.path.join(fontdir, 'KeepCalm-Medium.ttf'), 80)

# Only runs on Pi
if 'arm' not in platform.machine():
  print('Not ARM, quitting')
  sys.exit(0)

from lib.waveshare_epd import epd7in5_V2

epd = epd7in5_V2.EPD()
width = epd.width
height = epd.height

# Draw time module
def draw_date_and_time(image_draw):
  now = datetime.now()
  time_str = now.strftime("%H:%M")
  image_draw.text((10, 10), time_str, font = font_80, fill = 0)
  date_str = now.strftime("%B %d, %Y")
  image_draw.text((10, 95), date_str, font = font_48, fill = 0)

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
  draw_divider(image_draw, 13, 135, width - 26, 5)
  
  # Update display
  epd.display(epd.getbuffer(image))
  time.sleep(2)

# The main function
def main():
  epd.init()
  print('Ready')

  # Update once a minute
  while True:
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

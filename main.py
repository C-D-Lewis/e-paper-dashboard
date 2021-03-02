import platform
import sys
import os
import time
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

fontdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'font')

heading_pro_book_48 = ImageFont.truetype(os.path.join(fontdir, 'Heading-Pro-Book-trial.ttf'), 48)
heading_pro_book_64 = ImageFont.truetype(os.path.join(fontdir, 'Heading-Pro-Book-trial.ttf'), 64)

# Only runs on Pi
if 'arm' not in platform.machine():
  print('Not ARM, quitting')
  sys.exit(0)

from lib.waveshare_epd import epd7in5_V2

epd = epd7in5_V2.EPD()
width = epd.width
height = epd.height

# Initialise the display
def init():
  epd.init()
  epd.Clear()
  print('Cleared')

# Draw things
def draw():
  # Prepare
  image = Image.new('1', (epd.width, epd.height), 255)  # Mode = 1bit
  draw = ImageDraw.Draw(image)
  draw.rectangle((0, 0, epd.width, epd.height), fill = 255)

  # Draw content
  now = datetime.now()
  time_str = now.strftime("%H:%M")
  draw.text((10, 0), 'Hello there, mum! Enjoy the bath!', font = heading_pro_book_48, fill = 0)
  draw.text((10, 100), 'I SAY I SAY I SAY', font = heading_pro_book_64, fill = 0)
  
  # Update display
  epd.display(epd.getbuffer(image))
  time.sleep(2)

# Send display to sleep (avoid damage)
def sleep():
  epd.sleep()
  print('Sleeping')

# The main function
def main():
  print('Starting')
  init()

  # Update once a minute
  # while True:
  draw()
  sleep()
    # time.sleep(60)

if __name__ in '__main__':
  try:
    main()
  except KeyboardInterrupt:    
    print('Exiting')
    epd7in5_V2.epdconfig.module_exit()
    exit()

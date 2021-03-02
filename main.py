import platform
import sys
import os
from PIL import Image, ImageDraw, ImageFont

fontdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'font')

heading_pro_book_24 = ImageFont.truetype(os.path.join(fontdir, 'Heading-Pro-Book-trial.ttf'), 24)

# Only runs on Pi
if 'arm' not in platform.machine():
  print('Not ARM, quitting')
  sys.exit(0)

from lib.waveshare_epd import epd7in5_V2

display = epd7in5_V2.EPD()

def init():
  
  display.init()
  display.Clear()
  print('Cleared')

#
def low_power():
  display.sleep()
  print('Sleeping')

def main():
  print('Starting')
  init()
  low_power()

if __name__ in '__main__':
  main()

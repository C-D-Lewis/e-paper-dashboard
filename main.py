import platform
import sys

# Only runs on Pi
if 'arm' not in platform.machine():
  print('Not ARM, quitting')
  sys.exit(0)

from lib.waveshare_epd import epd7in5_V2
from PIL import Image,ImageDraw,ImageFont

def main():
  print('Starting')

if __name__ in '__main__':
  main()

import platform
import time
from PIL import Image, ImageDraw

# Allow testing on non-pi devices
RUNNING_ON_PI = 'arm' in platform.machine()
print({ 'RUNNING_ON_PI': RUNNING_ON_PI })

# Only runs on Pi
print('[epaper] EPD import')
if RUNNING_ON_PI:
  from lib.waveshare_epd import epd7in5_V2
  epd = epd7in5_V2.EPD()
  DISP_WIDTH = epd.width
  DISP_HEIGHT = epd.height
else:
  DISP_WIDTH = 800
  DISP_HEIGHT = 480

#
# Initialise the display
#
def init():
  print('[epaper] epd.init()')
  if RUNNING_ON_PI:
    epd.init()

#
# Prepare to draw
#
def prepare():
  image = Image.new('1', (DISP_WIDTH, DISP_HEIGHT), 255)  # Mode = 1bit
  image_draw = ImageDraw.Draw(image)
  image_draw.rectangle((0, 0, DISP_WIDTH, DISP_HEIGHT), fill = 255)

  return image, image_draw

#
# Handle updating the display
#
def show(image):
  print('[epaper] epd.display()')
  if RUNNING_ON_PI:
    epd.display(epd.getbuffer(image))
  else:
    image.save('render.png')
  print('[epaper] epd.display() complete')
  
#
# Handle sleeping the display
#
def sleep():
  print('[epaper] epd.sleep()')
  if RUNNING_ON_PI:
    time.sleep(2)
    epd.sleep()
  print('[epaper] epd.sleep() complete')

#
# Handle deinitialising the display
#
def deinit():
  print('[epaper] module_exit()')
  if RUNNING_ON_PI:
    epd7in5_V2.epdconfig.module_exit()

import platform
import time
from PIL import Image, ImageDraw
from modules import log

# Allow testing on non-pi devices
RUNNING_ON_PI = 'arm' in platform.machine()
log.info('epaper', { RUNNING_ON_PI })

# Only runs on Pi
log.debug('epaper', 'EPD import')
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
  log.debug('epaper', 'epd.init()')
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
  log.debug('epaper', 'epd.display()')
  if RUNNING_ON_PI:
    epd.display(epd.getbuffer(image))
  else:
    image.save('render.png')
  log.debug('epaper', 'epd.display() complete')
  
#
# Handle sleeping the display
#
def sleep():
  log.debug('epaper', 'epd.sleep()')
  if RUNNING_ON_PI:
    time.sleep(2)
    epd.sleep()
  log.debug('epaper', 'epd.sleep() complete')

#
# Handle deinitialising the display
#
def deinit():
  log.debug('epaper', 'module_exit()')
  if RUNNING_ON_PI:
    epd7in5_V2.epdconfig.module_exit()

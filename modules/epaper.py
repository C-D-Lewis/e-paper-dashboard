import platform
from PIL import Image, ImageDraw

RUNNING_ON_PI = 'arm' in platform.machine()
print({ 'RUNNING_ON_PI': RUNNING_ON_PI })

# Only runs on Pi
if RUNNING_ON_PI:
  from lib.waveshare_epd import epd7in5_V2
  epd = epd7in5_V2.EPD()
  disp_width = epd.width
  disp_height = epd.height
else:
  print('[TEST] EPD import')
  disp_width = 800
  disp_height = 480

# Initialise the display
def init():
  if RUNNING_ON_PI:
    epd.init()
  else:
    print('[TEST] epd.init()')

# Prepare to draw
def prepare():
  image = Image.new('1', (disp_width, disp_height), 255)  # Mode = 1bit
  image_draw = ImageDraw.Draw(image)
  image_draw.rectangle((0, 0, disp_width, disp_height), fill = 255)

  return image, image_draw

# Handle updating the display
def show(image):
  if RUNNING_ON_PI:
    epd.display(epd.getbuffer(image))
  else:
    image.save('render.png')
    print('[TEST] epd.display()')

# Handle sleeping the display
def sleep():
  if RUNNING_ON_PI:
    epd.sleep()
  else:
    print('[TEST] epd.sleep()')

# Handle deinitialising the display
def deinit():
  if RUNNING_ON_PI:
    epd7in5_V2.epdconfig.module_exit()
  else:
    print('[TEST] module_exit()')

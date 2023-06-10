import os
import time
from datetime import datetime
from modules import fonts, helpers, epaper, timer, config, log
from modes.hourly import run_hourly
from modes.minutely import run_minutely
from modules.constants import DIVIDER_SIZE, WIDGET_BOUNDS_LEFT_BOTTOM, WIDGET_BOUNDS_RIGHT, WIDGET_BOUNDS_TOP, WIDGET_BOUNDS_LEFT_TOP, MIDWAY

config.require(['MODE'])

################################## Main loop ###################################

#
# The main function
#
def main():
  mode = config.get('MODE')

  if mode == 'hourly':
    run_hourly()
  elif mode == 'minutely':
    run_minutely()
  else:
    raise Exception(f'Invalid mode: {mode}')

if __name__ in '__main__':
  try:
    main()
  except KeyboardInterrupt:
    log.error('main', 'Exiting')
    epaper.deinit()
    exit()

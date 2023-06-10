import os
import time
from datetime import datetime
from modules import fonts, helpers, epaper, timer, config, log
from widgets.DateTimeWidget import DateTimeWidget
from widgets.WeatherWidget import WeatherWidget
from widgets.NewsWidget import NewsWidget
from widgets.ForecastWidget import ForecastWidget

# Top widget
TOP_WIDGET = { 'widget': DateTimeWidget('hourly'), 'interval': 1 }
# Left widget
LEFT_WIDGET = {}
# Right widget
RIGHT_WIDGET = {}

################################## Main loop ###################################

#
# Draw all the things
#
def draw():
  timer.start()
  image, image_draw = epaper.prepare()

  # Draw all sections
  TOP_WIDGET['widget'].draw(image_draw, image)
  # LEFT_WIDGET['widget'].draw(image_draw, image)
  # RIGHT_WIDGET['widget'].draw(image_draw, image)

  # Update display
  epaper.show(image)
  timer.end('main draw')
  time.sleep(2)

#
# Wait for the next hour to start
#
def wait_for_next_hour():
  now = datetime.now()
  while now.minute != 0 and now.second != 0:
    now = datetime.now()
    time.sleep(1)

#
# Run in hourly mode, summary data only
#
def run_hourly():
  # Initial update and draw
  timer.start()
  TOP_WIDGET['widget'].update_data()
  # LEFT_WIDGET['widget'].update_data()
  # RIGHT_WIDGET['widget'].update_data()
  timer.end('initial update')
  epaper.init()
  draw()
  epaper.sleep()

  # Update once a minute forever
  while True:
    try:
      wait_for_next_hour()

      # Update once per hour, summary data only
      TOP_WIDGET['widget'].update_data()
      # LEFT_WIDGET['widget'].update_data()
      # RIGHT_WIDGET['widget'].update_data()
    except Exception as err:
      # Failed to work normally
      log.error('main', err)
      time.sleep(5)

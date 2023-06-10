import os
import time
from datetime import datetime
from modules import fonts, helpers, epaper, timer, config, log
from widgets.DateTimeWidget import DateTimeWidget
from widgets.WeatherWidget import WeatherWidget
from widgets.NewsWidget import NewsWidget
from widgets.ForecastWidget import ForecastWidget
from modules.constants import WIDGET_BOUNDS_LEFT, WIDGET_BOUNDS_RIGHT

# Top 'left' widget
TOP_LEFT_WIDGET = DateTimeWidget('hourly')
# Top right widget
TOP_RIGHT_WIDGET = WeatherWidget()
# Left widget
LEFT_WIDGET = NewsWidget(WIDGET_BOUNDS_LEFT)
# Right widget
RIGHT_WIDGET = ForecastWidget(WIDGET_BOUNDS_RIGHT)

################################## Main loop ###################################

#
# Draw all the things
#
def draw():
  timer.start()
  image, image_draw = epaper.prepare()

  # Draw all sections
  TOP_LEFT_WIDGET.draw(image_draw, image)
  TOP_RIGHT_WIDGET.draw(image_draw, image)
  LEFT_WIDGET.draw(image_draw, image)
  RIGHT_WIDGET.draw(image_draw, image)

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
  TOP_LEFT_WIDGET.update_data()
  TOP_RIGHT_WIDGET.update_data()
  LEFT_WIDGET.update_data()
  RIGHT_WIDGET.update_data()
  timer.end('initial update')
  epaper.init()
  draw()
  epaper.sleep()

  # Update once a minute forever
  while True:
    try:
      wait_for_next_hour()

      # Update once per hour, summary data only
      TOP_LEFT_WIDGET.update_data()
      TOP_RIGHT_WIDGET.update_data()
      LEFT_WIDGET.update_data()
      RIGHT_WIDGET.update_data()
    except Exception as err:
      # Failed to work normally
      log.error('main', err)
      time.sleep(5)

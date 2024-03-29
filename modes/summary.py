import os
import time
from datetime import datetime
from modules import fonts, helpers, epaper, timer, config, log
from widgets.DateTimeWidget import DateTimeWidget
from widgets.WeatherWidget import WeatherWidget
from widgets.NewsWidget import NewsWidget
from widgets.ForecastWidget import ForecastWidget
from modules.constants import WIDGET_BOUNDS_LEFT, WIDGET_BOUNDS_RIGHT
from copy import deepcopy

# Adjustments can be made here
NEWS_BOUNDS = (
  WIDGET_BOUNDS_LEFT[0],
  WIDGET_BOUNDS_LEFT[1] - 15,
  WIDGET_BOUNDS_LEFT[2] + 15,
  WIDGET_BOUNDS_LEFT[3]
)
FORECAST_BOUNDS = (
  WIDGET_BOUNDS_RIGHT[0],
  WIDGET_BOUNDS_RIGHT[1] - 15,
  WIDGET_BOUNDS_RIGHT[2],
  WIDGET_BOUNDS_RIGHT[3]
)

# Top 'left' widget
TOP_LEFT_WIDGET = DateTimeWidget()
# Top right widget
TOP_RIGHT_WIDGET = WeatherWidget()
# Left widget
LEFT_WIDGET = NewsWidget(NEWS_BOUNDS)
# Right widget
RIGHT_WIDGET = ForecastWidget(FORECAST_BOUNDS)

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
  while now.minute != 0 or now.second != 0:
    now = datetime.now()
    time.sleep(1)

#
# Run in summary mode, summary data only
#
def run_summary():
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
      timer.start()
      TOP_LEFT_WIDGET.update_data()
      TOP_RIGHT_WIDGET.update_data()
      LEFT_WIDGET.update_data()
      RIGHT_WIDGET.update_data()
      timer.end('main update')

      # Draw all widgets
      with helpers.timeout(seconds=45):
        epaper.init()
        draw()
        epaper.sleep()
    except Exception as err:
      # Failed to work normally
      log.error('main', err)
      time.sleep(5)

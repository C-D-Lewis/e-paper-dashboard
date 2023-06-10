import json
import os
import random
from datetime import datetime
from modules import fonts, helpers, fetch, log
from widgets.Widget import Widget
from modules.constants import WIDGET_BOUNDS_TOP

BOUNDS = WIDGET_BOUNDS_TOP

#
# DateTimeWidget class
#
class DateTimeWidget(Widget):
  #
  # Constructor
  #
  def __init__(self):
    super().__init__(BOUNDS)

    self.time_str = ''
    self.time_str = ''

  #
  # Update latest date and time
  #
  def update_data(self):
    try:
      now = datetime.now()
      self.time_str = now.strftime("%H:%M")
      self.date_str = now.strftime("%a %-d %b %Y")

      log.info('datetime', f"{self.time_str} {self.date_str}")
      self.unset_error()
    except Exception as err:
      self.set_error(err)

  #
  # Draw the date and time
  #
  def draw_data(self, image_draw, image):
    root_x = 8
    root_y = 10

    image_draw.text((root_x, root_y), self.time_str, font = fonts.KEEP_CALM_80, fill = 0)
    image_draw.text((root_x, root_y + 87), self.date_str, font = fonts.KEEP_CALM_46, fill = 0)

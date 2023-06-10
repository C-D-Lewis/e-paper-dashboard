import json
import os
import random
from datetime import datetime
from modules import fonts, helpers, fetch, log
from widgets.Widget import Widget
from modules.constants import WIDGET_BOUNDS_LEFT_BOTTOM

BOUNDS = WIDGET_BOUNDS_LEFT_BOTTOM

#
# OnThisDayWidget class
#
class OnThisDayWidget(Widget):
  #
  # Constructor
  #
  def __init__(self):
    super().__init__(BOUNDS)

    self.content = {}

  #
  # Update latest tweet
  #
  def update_data(self):
    try:
      now = datetime.now()
      ddmm_str = now.strftime("%m/%d")

      # Fetch data
      url = f'https://en.wikipedia.org/api/rest_v1/feed/onthisday/selected/{ddmm_str}'
      res = fetch.fetch_json(url, {
        'User-Agent': 'github.com/c-d-lewis/e-paper-display'
      })

      # Pick random item
      selections = res['selected']
      index = random.randint(0, len(selections) - 1)
      self.content = selections[index]['text']

      log.info('onthisday', self.content)
      self.unset_error()
    except Exception as err:
      self.set_error(err)

  #
  # Draw the content
  #
  def draw_data(self, image_draw, image):
    root_x = self.bounds[0] + 5
    root_y = self.bounds[1] + 10
    line_gap_y = 20
    max_line_width = self.bounds[2] - 10
    font = fonts.KEEP_CALM_20

    # Title
    image_draw.text((root_x + 110, root_y - 5), "On This Day", font = fonts.KEEP_CALM_24, fill = 0)
    image_draw.rectangle([root_x + 110, root_y + 20, root_x + 241, root_y + 22], fill = 0)

    # Content, wrapped
    content = f"\"{self.content}\""
    paragraph_y = root_y + 26
    lines = helpers.get_wrapped_lines(content, font, max_line_width)
    for index, line in enumerate(lines):
      image_draw.text((root_x, paragraph_y + (index * line_gap_y)), line, font = font, fill = 0)

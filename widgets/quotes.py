from PIL import Image, ImageDraw, ImageOps
import datetime
import json
import os
import random

from modules import fetch, fonts, config, helpers, images
from widgets.Widget import Widget
from modules.constants import WIDGET_BOUNDS

QUOTES_BOUNDS = WIDGET_BOUNDS[2]

# Max lines to a quote
MAX_LINES = 7

#
# QuotesWidget class
#
class QuotesWidget(Widget):
  #
  # Constructor
  #
  def __init__(self):
    super().__init__(QUOTES_BOUNDS)

    self.quote = {}

    # Load quotes file
    file_path = os.path.join(os.path.dirname(__file__), '../data/quotes.json')
    with open(file_path) as json_file:
      self.quote_list = json.load(json_file)

  #
  # Update latest tweet
  #
  def update_data(self):
    try:
      # Choose a quote
      index = random.randint(0, len(self.quote_list))
      self.quote = self.quote_list[index]

      print(f"quotes: {self.quote}")
      self.unset_error()
    except Exception as err:
      self.set_error(err)

  #
  # Draw the news stories
  #
  def draw(self, image_draw):
    if self.error:
      self.draw_error(image_draw)
      return

    try:
      root_y = self.bounds[1] + 5
      line_gap_y = 25

      # Quote content, wrapped
      content = f"\"{self.quote['text']}\""
      content_x = self.bounds[0]
      paragraph_y = root_y + 5
      lines = helpers.get_wrapped_lines(content, fonts.KEEP_CALM_24, self.bounds[2])
      font = fonts.KEEP_CALM_20 if len(lines) > MAX_LINES else fonts.KEEP_CALM_24
      lines = helpers.get_wrapped_lines(content, font, self.bounds[2])
      for index, line in enumerate(lines):
        image_draw.text((content_x, paragraph_y + (index * line_gap_y)), line, font = font, fill = 0)

      # Author, after text
      paragraph_height = helpers.get_paragraph_height(content, font, self.bounds[2], line_gap_y)
      line_y = paragraph_y + paragraph_height + 5
      author_str = f"                       -- {self.quote['author']}"
      image_draw.text((content_x, line_y), author_str, font = fonts.KEEP_CALM_20, fill = 0)
    except Exception as err:
      self.set_error(err)
      self.draw_error(image_draw)

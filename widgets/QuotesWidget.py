import json
import os
import random
from modules import fonts, helpers
from widgets.Widget import Widget
from modules.constants import WIDGET_BOUNDS_RIGHT

QUOTES_BOUNDS = WIDGET_BOUNDS_RIGHT

# Debug quote
DEBUG_QUOTE = "This is just an unbelieveably long and inspiring quote. Some say that even reading this quote could change the course of history, settle a territorial dispute, or right unforgivable wrongs. It's so powerful that we can only use it for testing this widget without endangering anybody. In fact nobody would even believe you could fit this into a maximum of 7 lines..."
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

      print(f"[quotes] {self.quote}")
      self.unset_error()
    except Exception as err:
      self.set_error(err)

  #
  # Draw the quote
  #
  def draw_data(self, image_draw, image):
    root_x = self.bounds[0] + 5
    root_y = self.bounds[1] + 10
    line_gap_y = 25
    max_line_width = self.bounds[2] - 10

    # Quote content, wrapped
    content = f"\"{self.quote['text']}\""
    paragraph_y = root_y + 5
    lines = helpers.get_wrapped_lines(content, fonts.KEEP_CALM_24, max_line_width)
    font = fonts.KEEP_CALM_20 if len(lines) > MAX_LINES else fonts.KEEP_CALM_24
    lines = helpers.get_wrapped_lines(content, font, max_line_width)
    for index, line in enumerate(lines):
      image_draw.text((root_x, paragraph_y + (index * line_gap_y)), line, font = font, fill = 0)

    # Author, after text
    paragraph_height = helpers.get_paragraph_height(content, font, max_line_width, line_gap_y)
    line_y = paragraph_y + paragraph_height
    author_str = f"                   -- {self.quote['author']}"
    image_draw.text((root_x, line_y), author_str, font = fonts.KEEP_CALM_20, fill = 0)

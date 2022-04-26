from modules import fetch, images, helpers, fonts
from widgets.Widget import Widget
from modules.constants import WIDGET_BOUNDS

RAIL_BOUNDS = WIDGET_BOUNDS[0]

#
# Get operator status from the page body fetched
#
def parse_operator_status(body, name):
  start = body.index(f"{name}</td>")
  temp = body[start:]
  start = temp.index('<td>') + len('<td>')
  temp = temp[start:]
  end = temp.index('</td>')
  return temp[:end]

#
# Fetch rail operator status
#
def fetch_status_page():
  url = 'http://www.nationalrail.co.uk/service_disruptions/indicator.aspx'
  headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:88.0) Gecko/20100101 Firefox/88.0'
  }
  return fetch.fetch_text(url, headers)

#
# RailWidget class
#
class RailWidget(Widget):
  #
  # Constructor
  #
  def __init__(self):
    super().__init__(RAIL_BOUNDS)

    self.tfl_rail = 'Unknown'
    self.greater_anglia = 'Unknown'

  #
  # Fetch rail network delays status
  #
  def update_data(self):
    try:
      body = fetch_status_page()

      # Parse
      self.tfl_rail = parse_operator_status(body, 'TfL Rail')
      self.greater_anglia = parse_operator_status(body, 'Greater Anglia')

      print(f"[rail] {self.tfl_rail} {self.greater_anglia}")
      self.unset_error()
    except Exception as err:
      self.set_error(err)

  #
  # Draw rail statuses
  #
  def draw_data(self, image_draw, image):
    text_x = 90
    text_gap = 25
    max_line_width = self.bounds[2] - text_x + 40

    # TfL Rail
    image.paste(images.ICON_TFL, (self.bounds[0], 175))
    lines = helpers.get_wrapped_lines(self.tfl_rail, fonts.KEEP_CALM_28, max_line_width)[:2]
    font = fonts.KEEP_CALM_24 if len(lines) > 1 else fonts.KEEP_CALM_28
    if len(lines) > 1:
      for index, line in enumerate(lines):
        image_draw.text((text_x, 185 + (index * text_gap)), line, font = font, fill = 0)
    else:
      image_draw.text((text_x, 194), self.tfl_rail, font = font, fill = 0)

    # GreaterAnglia
    image.paste(images.ICON_GA, (self.bounds[0], 239))
    lines = helpers.get_wrapped_lines(self.greater_anglia, fonts.KEEP_CALM_28, max_line_width)[:2]
    font = fonts.KEEP_CALM_24 if len(lines) > 1 else fonts.KEEP_CALM_28
    if len(lines) > 1:
      for index, line in enumerate(lines):
        image_draw.text((text_x, 245 + (index * text_gap)), line, font = font, fill = 0)
    else:
      image_draw.text((text_x, 258), self.greater_anglia, font = font, fill = 0)

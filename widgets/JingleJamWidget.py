from datetime import datetime
from modules import fetch, fonts, images
from widgets.Widget import Widget
from modules.constants import WIDGET_BOUNDS_BOTTOM_LEFT

BOUNDS = WIDGET_BOUNDS_BOTTOM_LEFT

#
# JingleJamWidget class
#
class JingleJamWidget(Widget):
  #
  # Constructor
  #
  def __init__(self):
    super().__init__(BOUNDS)

    self.data = {
      'amount': 0,
      'amount_last_hour': 0
    }

  #
  # Update Jingle Jam raised amount
  #
  def update_data(self):
    try:
      # Fetch latest data
      url = 'https://dashboard.jinglejam.co.uk/api/tiltify'
      json = fetch.fetch_json(url, {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0'
      })
      new_amount = round(json['total']['pounds'])

      # Derive application values
      self.data['amount'] = new_amount

      # Since last hour
      now = datetime.now()
      if now.minute == 0:
        self.data['amount_last_hour'] = new_amount

      print(f"[jinglejam] {self.data}")
      self.unset_error()
    except Exception as err:
      self.set_error(err)

  #
  # Draw amount raised
  #
  def draw_data(self, image_draw, image):
    root_x = self.bounds[0] + 10
    root_y = self.bounds[1] + 5
    image_x = round((self.bounds[2] - 250) / 2)
    text_x = root_x + 40

    # Logo
    image.paste(images.JINGLE_JAM, (image_x, root_y))

    # Amount raised
    image_draw.text((text_x, root_y + 80), f"£{self.data['amount']:,}", font = fonts.KEEP_CALM_46, fill = 0)

    # Amount this hour
    this_hour = round(self.data['amount'] - self.data['amount_last_hour'])
    image_draw.text((text_x, root_y + 125), f"+ £{this_hour:,}", font = fonts.KEEP_CALM_24, fill = 0)

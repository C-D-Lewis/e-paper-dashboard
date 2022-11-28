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
      # url = f""
      # html = fetch.fetch_text(url)
      new_amount = ...

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
    this_hour = self.data['amount'] - self.data['amount_last_hour']
    image_draw.text((text_x, root_y + 123), f"+ £{self.data['amount_last_hour']:,}", font = fonts.KEEP_CALM_24, fill = 0)

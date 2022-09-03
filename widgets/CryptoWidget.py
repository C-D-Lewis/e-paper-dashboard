import time
import random
from modules import fetch, config, fonts, images, constants
from widgets.Widget import Widget
from modules.constants import WIDGET_BOUNDS_BOTTOM_LEFT

BOUNDS = WIDGET_BOUNDS_BOTTOM_LEFT

#
# CryptoWidget class
#
class CryptoWidget(Widget):
  #
  # Constructor
  #
  def __init__(self):
    super().__init__(BOUNDS)

    self.btc_data = { 'value': 0, 'change': 0 }
    self.eth_data = { 'value': 0, 'change': 0 }

  #
  # Update crypto portfolio
  #
  def update_data(self):
    # Random wait to avoid 1 rps limit at the same time as another running instance
    wait_time_s = random.randint(1, 4)
    print(f"[crypto] random wait for {wait_time_s}s")
    time.sleep(wait_time_s)

    # Fetch from Nomics API
    try:
      url = f"https://api.nomics.com/v1/currencies/ticker?key={config.get('NOMICS_KEY')}&ids=BTC,ETH&interval=1d,30d&convert=GBP"
      json = fetch.fetch_json(url)

      BTC_AMOUNT = config.get('BTC_AMOUNT')
      ETH_AMOUNT = config.get('ETH_AMOUNT')

      # Derive application values
      btc_res = json[0]
      self.btc_data['value'] = round(BTC_AMOUNT * float(btc_res['price']), 2)
      self.btc_data['change'] = round(BTC_AMOUNT * float(btc_res['1d']['price_change']), 2)
      self.btc_data['price_change_pct'] = round(float(btc_res['1d']['price_change_pct']) * 100, 1)
      eth_res = json[1]
      self.eth_data['value'] = round(ETH_AMOUNT * float(eth_res['price']), 2)
      self.eth_data['change'] = round(ETH_AMOUNT * float(eth_res['1d']['price_change']), 2)
      self.eth_data['price_change_pct'] = round(float(eth_res['1d']['price_change_pct']) * 100, 1)

      print(f"[crypto] {self.btc_data} {self.eth_data}")
      self.unset_error()
    except Exception as err:
      self.set_error(err)

  #
  # Draw the daily change
  #
  def draw_daily_change(self, image_draw, image):
    root_x = self.bounds[0] + 10
    root_y = self.bounds[1] + 10
    text_x = root_x + 80
    font = fonts.KEEP_CALM_28

    image.paste(images.ICON_BTC, (root_x, root_y + 5))
    arrow = '+' if self.btc_data['price_change_pct'] > 0 else '-'
    change_str = f"{arrow}{abs(self.btc_data['price_change_pct'])}% (24h)"
    image_draw.text((text_x, root_y + 25), change_str, font = font, fill = 0)

    image.paste(images.ICON_ETH, (root_x, root_y + 75))
    arrow = '+' if self.eth_data['price_change_pct'] > 0 else '-'
    change_str = f"{arrow}{abs(self.eth_data['price_change_pct'])}% (24h)"
    image_draw.text((text_x, root_y + 100), change_str, font = font, fill = 0)

  #
  # Draw earnings with configured portfolio values
  #
  def draw_earnings(self, image_draw, image):
    text_x = self.bounds[0] + 80
    font = fonts.KEEP_CALM_28

    image.paste(images.ICON_BTC, (self.bounds[0], self.bounds[1]))
    arrow = '+' if self.btc_data['change'] > 0 else '-'
    value_str = f"£{self.btc_data['value']}"
    change_str = f"{arrow}{abs(self.btc_data['change'])}"
    image_draw.text((text_x, self.bounds[1] + 20), f"{value_str} ({change_str})", font = font, fill = 0)

    image.paste(images.ICON_ETH, (self.bounds[0], self.bounds[1] + 74))
    arrow = '+' if self.eth_data['change'] > 0 else '-'
    value_str = f"£{self.eth_data['value']}"
    change_str = f"{arrow}{abs(self.eth_data['change'])}"
    image_draw.text((text_x, self.bounds[1] + 94), f"{value_str} ({change_str})", font = font, fill = 0)

  #
  # Draw crypto widget
  # - Note: Uses any widget bounds
  #
  def draw_data(self, image_draw, image):
    DISPLAY_MODE = config.get('CRYPTO_DISPLAY_MODE')  # 'daily_change' or 'earnings'
    if DISPLAY_MODE == 'daily_change':
      self.draw_daily_change(image_draw, image)
    elif DISPLAY_MODE == 'earnings':
      self.draw_earnings(image_draw, image)
    else:
      raise Exception('No crypto mode selected')

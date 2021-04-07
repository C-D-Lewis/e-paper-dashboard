from modules import fetch, config, fonts, images, constants
from widgets.Widget import Widget
from modules.constants import WIDGET_BOUNDS

CRYPTO_BOUNDS = WIDGET_BOUNDS[1]

# CryptoWidget class
class CryptoWidget(Widget):
  # Constructor
  def __init__(self):
    super().__init__(CRYPTO_BOUNDS)
    self.btc_data = { 'value': 0, 'change': 0 }
    self.eth_data = { 'value': 0, 'change': 0 }

  # Update crypto portfolio
  def update_data(self):
    try:
      url = f"https://api.nomics.com/v1/currencies/ticker?key={config.get('NOMICS_KEY')}&ids=BTC,ETH&interval=1d,30d&convert=GBP"
      json = fetch.fetch_json(url)

      btc_amount = config.get('BTC_AMOUNT')
      eth_amount = config.get('ETH_AMOUNT')

      btc_res = json[0]
      self.btc_data['value'] = round(btc_amount * float(btc_res['price']), 2)
      self.btc_data['change'] = round(btc_amount * float(btc_res['1d']['price_change']), 2)
      eth_res = json[1]
      self.eth_data['value'] = round(eth_amount * float(eth_res['price']), 2)
      self.eth_data['change'] = round(eth_amount * float(eth_res['1d']['price_change']), 2)

      print(f"crypto: {self.btc_data} {self.eth_data}")
      self.unset_error()
    except Exception as err:
      self.set_error(err)

  # Draw crypto values
  def draw(self, image_draw, image):
    if self.error:
      self.draw_error(image_draw)
      return

    try:
      text_x = 95
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
    except Exception as err:
      self.set_error(err)
      self.draw_error(image_draw)

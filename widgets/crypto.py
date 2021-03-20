from modules import fetch, config, fonts, images

data = {
  'BTC': { 'value': 0, 'change': 0 },
  'ETH': { 'value': 0, 'change': 0 }
}

# Update crypto portfolio
def update_data():
  try:
    url = f"https://api.nomics.com/v1/currencies/ticker?key={config.get('NOMICS_KEY')}&ids=BTC,ETH&interval=1d,30d&convert=GBP"
    json = fetch.fetch_json(url)

    btc_amount = config.get('BTC_AMOUNT')
    eth_amount = config.get('ETH_AMOUNT')

    btc_res = json[0]
    data['BTC']['value'] = round(btc_amount * float(btc_res['price']), 2)
    data['BTC']['change'] = round(btc_amount * float(btc_res['1d']['price_change']), 2)
    eth_res = json[1]
    data['ETH']['value'] = round(eth_amount * float(eth_res['price']), 2)
    data['ETH']['change'] = round(eth_amount * float(eth_res['1d']['price_change']), 2)
    print(f"crypto: {data}")
  except Exception as err:
    print('crypto.update_data error: {0}'.format(err))
    data['BTC']['value'] = 0
    data['BTC']['change'] = 0
    data['ETH']['value'] = 0
    data['ETH']['change'] = 0

# Draw crypto values
def draw(canvas, image):
  root_x = 15
  text_x = 95
  font = fonts.KEEP_CALM_28

  image.paste(images.ICON_BTC, (root_x, 335))
  arrow = '+' if data['BTC']['change'] > 0 else '-'
  value_str = f"£{data['BTC']['value']}"
  change_str = f"{arrow}{abs(data['BTC']['change'])}"
  canvas.text((text_x, 355), f"{value_str} ({change_str})", font = font, fill = 0)

  image.paste(images.ICON_ETH, (root_x, 409))
  arrow = '+' if data['ETH']['change'] > 0 else '-'
  value_str = f"£{data['ETH']['value']}"
  change_str = f"{arrow}{abs(data['ETH']['change'])}"
  canvas.text((text_x, 429), f"{value_str} ({change_str})", font = font, fill = 0)

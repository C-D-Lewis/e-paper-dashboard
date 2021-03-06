import images
from datetime import datetime

from modules import fetch, helpers, fonts, images

DAY_START_HOUR = 6
DAY_END_HOUR = 18

data = {
  'current_temp': 0,
  'current_summary': 'unknown',
  'current_icon': 'unknown',
  'temp_high': 0,
  'temp_low': 0
}

# Get an appropriate weather icon
def get_icon():
  current_icon = data['current_icon'].lower()
  now = datetime.now()
  hours = now.hour
  is_daytime = hours > DAY_START_HOUR and hours < DAY_END_HOUR

  if 'cloud' in current_icon or 'overcast' in current_icon:
    return images.ICON_CLOUD_DAY if is_daytime else images.ICON_CLOUD_NIGHT
  if 'wind' in current_icon:
    return images.ICON_WIND
  if 'rain' in current_icon:
    return images.ICON_RAIN
  if 'clear' in current_icon or 'sun' in current_icon:
    return images.ICON_CLEAR_DAY if is_daytime else images.ICON_CLEAR_NIGHT
  if 'thunder' in current_icon or 'storm' in current_icon or 'lighting' in current_icon:
    return images.ICON_STORM
  if 'snow' in current_icon:
    return images.ICON_SNOW
  if 'ice' in current_icon or 'frost' in current_icon:
    return images.ICON_FROST
  if 'mist' in current_icon or 'fog' in current_icon or 'haz' in current_icon:
    return images.ICON_FOG

  if 'error' in current_icon:
    return images.ICON_ERROR
  return images.ICON_QUESTION_MARK

# Update weather data
def update_data():
  try:
    url = f"https://api.darksky.net/forecast/{helpers.config['DARKSKY_KEY']}/{helpers.config['LATITUDE']},{helpers.config['LONGITUDE']}?units=auto&exclude=hourly,minutely"
    new_data = fetch.fetch_json(url)
    data['current_temp'] = round(new_data['currently']['apparentTemperature'])
    data['current_summary'] = new_data['currently']['summary']
    data['current_icon'] = new_data['currently']['icon']
    data['temp_high'] = round(new_data['daily']['data'][0]['apparentTemperatureHigh'])
    data['temp_low'] = round(new_data['daily']['data'][0]['apparentTemperatureLow'])
    print(data)
  except Exception as err:
    print("weather.update_data error: {0}".format(err))
    data['current_temp'] = '!'
    data['current_summary'] = 'error'
    data['current_icon'] = 'error'
    data['temp_high'] = '!'
    data['temp_low'] = '!'

# Draw the weather icon, temperature, and conditions
def draw(canvas, image):
  image.paste(get_icon(), (520, 10))
  temp_str = f"{data['current_temp']}°C"
  canvas.text((660, 30), temp_str, font = fonts.KEEP_CALM_48, fill = 0)
  temp_high_low_str = f"{data['temp_high']} | {data['temp_low']}"
  canvas.text((660, 85), temp_high_low_str, font = fonts.KEEP_CALM_28, fill = 0)

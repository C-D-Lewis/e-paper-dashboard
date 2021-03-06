import images
from datetime import datetime

from modules import fetch, helpers, fonts, images, config

DAY_START_HOUR = 6
DAY_END_HOUR = 18

data = {
  'current_temp': 0,
  'current_summary': 'unknown',
  'current_icon': 'unknown',
  'current_wind_speed': 0,
  'current_humidity': 0,
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
    url = f"https://api.darksky.net/forecast/{config.get('DARKSKY_KEY')}/{config.get('LATITUDE')},{config.get('LONGITUDE')}?units=auto&exclude=hourly,minutely"
    res = fetch.fetch_json(url)
    # print(res)

    data['current_temp'] = round(res['currently']['apparentTemperature'])
    data['current_summary'] = res['currently']['summary']
    data['current_icon'] = res['currently']['icon']
    data['current_wind_speed'] = res['currently']['windSpeed']
    data['current_humidity'] = res['currently']['humidity']
    data['temp_high'] = round(res['daily']['data'][0]['apparentTemperatureHigh'])
    data['temp_low'] = round(res['daily']['data'][0]['apparentTemperatureLow'])
    print(f"weather: {data}")
  except Exception as err:
    print('weather.update_data error: {0}'.format(err))
    data['current_temp'] = '!'
    data['current_summary'] = 'error'
    data['current_icon'] = 'error'
    data['temp_high'] = '!'
    data['temp_low'] = '!'
    data['current_wind_speed'] = '!'
    data['current_humidity'] = '!'

# Draw the weather icon, temperature, and conditions
def draw(canvas, image):
  image.paste(get_icon(), (510, 10))
  temp_str = f"{data['current_temp']}°C"
  canvas.text((650, 20), temp_str, font = fonts.KEEP_CALM_48, fill = 0)
  temp_high_low_str = f"{data['temp_high']} | {data['temp_low']}"
  canvas.text((650, 75), temp_high_low_str, font = fonts.KEEP_CALM_28, fill = 0)

  # Smaller details
  image.paste(images.ICON_RAIN_32, (650, 115))

  image.paste(images.ICON_WINDSOCK, (700, 115))

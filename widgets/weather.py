import images
import datetime

from modules import fetch, helpers, fonts, images, config
from widgets import news

# Constants
DAY_START_HOUR = 6
DAY_END_HOUR = 18

data = {
  'current': {
    'temp': 0,
    'summary': 'unknown',
    'icon': 'unknown',
    'wind_speed': 0,
    'precip_prob': 0,
  },
  'forecast': [],
  'temp_high': 0,
  'temp_low': 0
}

# Get an appropriate weather icon
def get_icon():
  icon = data['current']['icon'].lower()
  hour = datetime.datetime.now().hour
  is_daytime = hour > DAY_START_HOUR and hour < DAY_END_HOUR

  if 'cloud' in icon or 'overcast' in icon:
    return images.ICON_CLOUD_DAY if is_daytime else images.ICON_CLOUD_NIGHT
  if 'wind' in icon:
    return images.ICON_WIND
  if 'rain' in icon:
    return images.ICON_RAIN
  if 'clear' in icon or 'sun' in icon:
    return images.ICON_CLEAR_DAY if is_daytime else images.ICON_CLEAR_NIGHT
  if 'thunder' in icon or 'storm' in icon or 'lighting' in icon:
    return images.ICON_STORM
  if 'snow' in icon:
    return images.ICON_SNOW
  if 'ice' in icon or 'frost' in icon:
    return images.ICON_FROST
  if 'mist' in icon or 'fog' in icon or 'haz' in icon:
    return images.ICON_FOG

  if 'error' in icon:
    return images.ICON_ERROR
  return images.ICON_QUESTION_MARK

# Get an appropriate weather icon for the forecast list
def get_forecast_icon(input):
  input_lower = input.lower()

  if 'cloud' in input_lower or 'overcast' in input_lower:
    return images.ICON_CLOUD_DAY_48
  if 'wind' in input_lower:
    return images.ICON_WIND
  if 'rain' in input_lower:
    return images.ICON_RAIN_48
  if 'clear' in input_lower or 'sun' in input_lower:
    return images.ICON_CLEAR_DAY_48
  if 'thunder' in input_lower or 'storm' in input_lower or 'lighting' in input_lower:
    return images.ICON_STORM
  if 'snow' in input_lower:
    return images.ICON_SNOW
  if 'ice' in input_lower or 'frost' in input_lower:
    return images.ICON_FROST
  if 'mist' in input_lower or 'fog' in input_lower or 'haz' in input_lower:
    return images.ICON_FOG

  if 'error' in input_lower:
    return images.ICON_ERROR
  return images.ICON_QUESTION_MARK

# Update weather data
def update_data():
  try:
    params = 'units=auto&exclude=hourly,minutely'
    url = f"https://api.darksky.net/forecast/{config.get('DARKSKY_KEY')}/{config.get('LATITUDE')},{config.get('LONGITUDE')}?{params}"
    json = fetch.fetch_json(url)

    # Current conditions
    currently = json['currently']
    data['current'] = {
      'temp': round(currently['apparentTemperature']),
      'summary': currently['summary'],
      'icon': currently['icon'],
      'wind_speed': round(currently['windSpeed']),
      'precip_prob': round(currently['precipProbability'] * 100)
    }
    daily = json['daily']['data'][0]
    data['temp_high'] = round(daily['apparentTemperatureHigh'])
    data['temp_low'] = round(daily['apparentTemperatureLow'])

    # 5 day forecast - first item is today
    for index in range(1, 6):
      day_data = json['daily']['data'][index]
      day = {
        'summary': day_data['summary'],
        'icon': day_data['icon'],
        'temp_high': round(day_data['apparentTemperatureHigh']),
        'temp_low': round(day_data['apparentTemperatureLow']),
        'precip_prob': round(day_data['precipProbability'] * 100),
        'wind_speed': round(day_data['windSpeed'])
      }
      data['forecast'].append(day)

    print(f"weather: {data}")
  except Exception as err:
    print('weather.update_data error: {0}'.format(err))
    data['current'] = {
      'temp': '!',
      'summary': 'error',
      'icon': 'error',
      'wind_speed': '!',
      'precip_prob': '!'
    }
    data['temp_high'] = '!'
    data['temp_low'] = '!'
    data['forecast'] = []

# Draw the weather icon, temperature, and conditions
def draw(canvas, image):
  root_x = 510
  root_y = 20
  text_x = 650

  image.paste(get_icon(), (root_x, root_y))
  temp_str = f"{data['current']['temp']}°C"
  canvas.text((text_x, root_y), temp_str, font = fonts.KEEP_CALM_48, fill = 0)
  temp_high_low_str = f"{data['temp_high']} | {data['temp_low']}"
  canvas.text((text_x, root_y + 55), temp_high_low_str, font = fonts.KEEP_CALM_28, fill = 0)

  # Smaller details
  font = fonts.KEEP_CALM_20
  detail_y = 115
  icon_y = detail_y + 8
  image.paste(images.ICON_RAIN_32, (text_x, detail_y))
  rain_chance_str = f"{data['current']['precip_prob']}"
  canvas.text((text_x + 35, icon_y), rain_chance_str, font = font, fill = 0)

  image.paste(images.ICON_WINDSOCK_32, (text_x + 80, detail_y))
  wind_speed_str = f"{data['current']['wind_speed']}"
  canvas.text((text_x + 115, icon_y), wind_speed_str, font = font, fill = 0)

# Draw 5 day forecast in the right hand section
def draw_forecast(canvas, image):
  root_x = 380
  root_y = 180
  gap_y = 60
  font = fonts.KEEP_CALM_20

  forecast = data['forecast']
  for index, day in enumerate(forecast):
    day_y = root_y + (index * gap_y)

    image.paste(get_forecast_icon(day['icon']), (root_x, day_y))

    canvas.text((root_x + 55, day_y + 25), day['summary'], font = font, fill = 0)

    # Get day of the week in string
    future_day = datetime.date.today() + datetime.timedelta(days = index + 1)
    future_dotw = helpers.get_weekday_name(future_day.weekday())

    day_temps_str = f"{future_dotw}: {day['temp_high']} | {day['temp_low']}"
    canvas.text((root_x + 55, day_y), day_temps_str, font = font, fill = 0)
    precip_str = f"{day['precip_prob']}%"
    canvas.text((root_x + 270, day_y), precip_str, font = font, fill = 0)
    speed_str = f"{day['wind_speed']}mph"
    canvas.text((root_x + 350, day_y), speed_str, font = font, fill = 0)

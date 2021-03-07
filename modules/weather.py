import images
import datetime

from modules import fetch, helpers, fonts, images, config, news

# Constants
DAY_START_HOUR = 6
DAY_END_HOUR = 18

data = {
  'current': {
    'temp': 0,
    'summary': 'unknown',
    'icon': 'unknown',
    'wind_speed': 0,
    'humidity': 0,
  },
  'forecast': [],
  'temp_high': 0,
  'temp_low': 0
}

# Get an appropriate weather icon
def get_icon(input):
  current_icon = input.lower()
  now = datetime.datetime.now()
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

# Get an appropriate weather icon for the forecast list
def get_forecast_icon(input):
  current_icon = input.lower()

  if 'cloud' in current_icon or 'overcast' in current_icon:
    return images.ICON_CLOUD_DAY_48
  if 'wind' in current_icon:
    return images.ICON_WIND
  if 'rain' in current_icon:
    return images.ICON_RAIN_48
  if 'clear' in current_icon or 'sun' in current_icon:
    return images.ICON_CLEAR_DAY_48
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

    # Current conditions
    data['current']['temp'] = round(res['currently']['apparentTemperature'])
    data['current']['summary'] = res['currently']['summary']
    data['current']['icon'] = res['currently']['icon']
    data['current']['wind_speed'] = round(res['currently']['windSpeed'])
    data['current']['precip_prob'] = round(res['currently']['precipProbability'] * 100)
    data['temp_high'] = round(res['daily']['data'][0]['apparentTemperatureHigh'])
    data['temp_low'] = round(res['daily']['data'][0]['apparentTemperatureLow'])

    # 5 day forecast - first item is today
    for index in range(1, 6):
      source = res['daily']['data'][index]
      day = {
        'summary': source['summary'],
        'icon': source['icon'],
        'temp_high': round(source['apparentTemperatureHigh']),
        'temp_low': round(source['apparentTemperatureLow']),
        'precip_prob': round(source['precipProbability'] * 100),
        'wind_speed': round(source['windSpeed'])
      }
      data['forecast'].append(day)

    print(f"weather: {data}")
  except Exception as err:
    print('weather.update_data error: {0}'.format(err))
    data['current']['temp'] = '!'
    data['current']['summary'] = 'error'
    data['current']['icon'] = 'error'
    data['current']['wind_speed'] = '!'
    data['current']['precip_prob'] = '!'
    data['temp_high'] = '!'
    data['temp_low'] = '!'
    data['forecast'] = []

# Draw the weather icon, temperature, and conditions
def draw(canvas, image):
  image.paste(get_icon(data['current']['icon']), (510, 10))
  temp_str = f"{data['current']['temp']}°C"
  canvas.text((650, 20), temp_str, font = fonts.KEEP_CALM_48, fill = 0)
  temp_high_low_str = f"{data['temp_high']} | {data['temp_low']}"
  canvas.text((650, 75), temp_high_low_str, font = fonts.KEEP_CALM_28, fill = 0)

  # Smaller details
  image.paste(images.ICON_RAIN_32, (650, 115))
  rain_chance_str = f"{data['current']['precip_prob']}%"
  canvas.text((685, 123), rain_chance_str, font = fonts.KEEP_CALM_20, fill = 0)

  image.paste(images.ICON_WINDSOCK, (725, 115))
  wind_speed_str = f"{data['current']['wind_speed']}"
  canvas.text((760, 123), wind_speed_str, font = fonts.KEEP_CALM_20, fill = 0)

# Draw 5 day forecast in the right hand section
def draw_forecast(canvas, image):
  root_x = 380
  root_y = 180
  gap_y = 60

  forecast = data['forecast']
  for index, day in enumerate(forecast):
    image.paste(get_forecast_icon(day['icon']), (root_x, root_y))

    canvas.text((root_x + 55, root_y + 25), day['summary'], font = fonts.KEEP_CALM_20, fill = 0)

    future_day = datetime.date.today() + datetime.timedelta(days = index + 1)
    future_dotw = helpers.get_weekday_name(future_day.weekday())
    day_temps_str = f"{future_dotw}: {day['temp_high']} | {day['temp_low']}"
    canvas.text((root_x + 55, root_y), day_temps_str, font = fonts.KEEP_CALM_20, fill = 0)
    precip_str = f"{day['precip_prob']}%"
    canvas.text((root_x + 270, root_y), precip_str, font = fonts.KEEP_CALM_20, fill = 0)
    speed_str = f"{day['wind_speed']}mph"
    canvas.text((root_x + 340, root_y), speed_str, font = fonts.KEEP_CALM_20, fill = 0)
      
    root_y += gap_y

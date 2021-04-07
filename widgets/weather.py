import images
import datetime

from modules import fetch, helpers, fonts, images, config
from widgets.Widget import Widget
from modules.constants import WIDGET_BOUNDS

WEATHER_BOUNDS = () # TODO

# Constants
DAY_START_HOUR = 6
DAY_END_HOUR = 18

# Get an appropriate weather icon
def get_icon(input):
  icon = input.lower()
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

# WeatherWidget class
class WeatherWidget(Widget):
  # Constructor
  def __init__(self):
    super().__init__(WEATHER_BOUNDS)

    self.current = {
      'temp': 0,
      'summary': 'unknown',
      'icon': 'unknown',
      'wind_speed': 0,
      'precip_prob': 0,
    }
    self.temp_high = 0
    self.temp_low = 0

  # Update weather data
  def update_data(self):
    try:
      params = 'units=auto&exclude=hourly,minutely'
      url = f"https://api.darksky.net/forecast/{config.get('DARKSKY_KEY')}/{config.get('LATITUDE')},{config.get('LONGITUDE')}?{params}"
      json = fetch.fetch_json(url)

      # Current conditions
      currently = json['currently']
      self.current = {
        'temp': round(currently['apparentTemperature']),
        'summary': currently['summary'],
        'icon': currently['icon'],
        'wind_speed': round(currently['windSpeed']),
        'precip_prob': round(currently['precipProbability'] * 100)
      }
      daily = json['daily']['data'][0]
      self.temp_high = round(daily['apparentTemperatureHigh'])
      self.temp_low = round(daily['apparentTemperatureLow'])

      print(f"weather: {self.current}")
      self.unset_error()
    except Exception as err:
      self.set_error(err)

  # Draw the weather icon, temperature, and conditions
  def draw(self, image_draw, image):
    if self.error:
      self.draw_error(image_draw)
      return

    try:
      root_x = 510
      root_y = 20
      text_x = 650

      image.paste(get_icon(self.current['icon']), (root_x, root_y))
      temp_str = f"{self.current['temp']}°C"
      image_draw.text((text_x, root_y), temp_str, font = fonts.KEEP_CALM_48, fill = 0)
      temp_high_low_str = f"{self.temp_high} | {self.temp_low}"
      image_draw.text((text_x, root_y + 55), temp_high_low_str, font = fonts.KEEP_CALM_28, fill = 0)

      # Smaller details
      font = fonts.KEEP_CALM_20
      detail_y = 115
      icon_y = detail_y + 8
      image.paste(images.ICON_RAIN_32, (text_x, detail_y))
      rain_chance_str = f"{self.current['precip_prob']}"
      image_draw.text((text_x + 35, icon_y), rain_chance_str, font = font, fill = 0)

      image.paste(images.ICON_WINDSOCK_32, (text_x + 80, detail_y))
      wind_speed_str = f"{self.current['wind_speed']}"
      image_draw.text((text_x + 115, icon_y), wind_speed_str, font = font, fill = 0)
    except Exception as err:
      self.set_error(err)
      self.draw_error(image_draw)

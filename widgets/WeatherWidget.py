import images
import datetime
from modules import fetch, fonts, images, config, log
from widgets.Widget import Widget
from modules.constants import DAY_START_HOUR, DAY_END_HOUR, MPH_PER_KPH

BOUNDS = (510, 20, 0, 0)

config.require(['LATITUDE', 'LONGITUDE', 'WEATHER_KEY'])

#
# Get an appropriate weather icon
#
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

#
# WeatherWidget class
#
class WeatherWidget(Widget):
  #
  # Constructor
  #
  def __init__(self):
    super().__init__(BOUNDS)

    self.current = {
      'temp': 0,
      'summary': 'unknown',
      'icon': 'unknown',
      'wind_speed': 0,
      'precip_prob': 0,
    }
    self.temp_high = 0
    self.temp_low = 0

  #
  # Update weather data
  #
  def update_data(self):
    try:
      url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{config.get('LATITUDE')}%2C{config.get('LONGITUDE')}?unitGroup=metric&include=current%2Cdays&key={config.get('WEATHER_KEY')}&contentType=json"
      json = fetch.fetch_json(url)
      # log.debug('weather', json)

      # Current conditions
      current = json['currentConditions']
      self.current = {
        'temp': round(current['temp']),
        'summary': current['conditions'],
        'icon': current['icon'],
        'wind_speed': round(current['windspeed'] * MPH_PER_KPH),
        'precip_prob': round(current['precipprob'] * 100)
      }

      # Today
      daily = json['days'][0]
      self.temp_high = round(daily['tempmax'])
      self.temp_low = round(daily['tempmin'])

      log.info('weather', self.current)
      self.unset_error()
    except Exception as err:
      self.set_error(err)

  #
  # Draw the weather icon, temperature, and conditions
  #
  def draw_data(self, image_draw, image):
    text_x = 650

    # Conditions headline and icon
    image.paste(get_icon(self.current['icon']), (self.bounds[0] + 8, self.bounds[1]))
    temp_str = f"{self.current['temp']}°C"
    image_draw.text((text_x, self.bounds[1]), temp_str, font = fonts.KEEP_CALM_48, fill = 0)
    temp_high_low_str = f"{self.temp_high} | {self.temp_low}"
    image_draw.text((text_x, self.bounds[1] + 58), temp_high_low_str, font = fonts.KEEP_CALM_28, fill = 0)

    # Smaller details for rain chance and wind speed
    font = fonts.KEEP_CALM_20
    detail_y = self.bounds[1] + 95
    icon_y = detail_y + 8
    image.paste(images.ICON_RAIN_32, (text_x, detail_y))
    rain_chance_str = f"{self.current['precip_prob']}"
    image_draw.text((text_x + 35, icon_y), rain_chance_str, font = font, fill = 0)
    image.paste(images.ICON_WINDSOCK_32, (text_x + 80, detail_y))
    wind_speed_str = f"{self.current['wind_speed']}"
    image_draw.text((text_x + 115, icon_y), wind_speed_str, font = font, fill = 0)

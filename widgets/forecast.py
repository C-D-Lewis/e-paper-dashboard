import images
import datetime
from modules import fetch, helpers, fonts, images, config
from widgets.Widget import Widget
from modules.constants import WIDGET_BOUNDS

FORECAST_BOUNDS = WIDGET_BOUNDS[2]

#
# Get an appropriate weather icon for the forecast list
#
def get_forecast_icon(input):
  icon = input.lower()

  if 'cloud' in icon or 'overcast' in icon:
    return images.ICON_CLOUD_DAY_48
  if 'wind' in icon:
    return images.ICON_WIND_48
  if 'rain' in icon:
    return images.ICON_RAIN_48
  if 'clear' in icon or 'sun' in icon:
    return images.ICON_CLEAR_DAY_48
  if 'thunder' in icon or 'storm' in icon or 'lighting' in icon:
    return images.ICON_STORM_48
  if 'snow' in icon:
    return images.ICON_SNOW_48
  if 'ice' in icon or 'frost' in icon:
    return images.ICON_FROST_48
  if 'mist' in icon or 'fog' in icon or 'haz' in icon:
    return images.ICON_FOG_48

  if 'error' in icon:
    return images.ICON_ERROR
  return images.ICON_QUESTION_MARK

#
# ForecastWidget class
#
class ForecastWidget(Widget):
  #
  # Constructor
  #
  def __init__(self):
    super().__init__(FORECAST_BOUNDS)

    self.forecast = []

  #
  # Update forecast data
  #
  def update_data(self):
    try:
      # Fetch data
      params = 'units=auto&exclude=hourly,minutely'
      url = f"https://api.darksky.net/forecast/{config.get('DARKSKY_KEY')}/{config.get('LATITUDE')},{config.get('LONGITUDE')}?{params}"
      json = fetch.fetch_json(url)

      # 5 day forecast - first item is today, so skip it
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
        self.forecast.append(day)

      print(f"forecast: {self.forecast}")
      self.unset_error()
    except Exception as err:
      self.set_error(err)

  #
  # Draw 5 day forecast list
  #
  def draw(self, image_draw, image):
    if self.error:
      self.draw_error(image_draw)
      return

    try:
      root_y = self.bounds[1] + 10
      gap_y = 60
      font = fonts.KEEP_CALM_20

      forecast = self.forecast
      for index, day in enumerate(forecast):
        day_y = root_y + (index * gap_y)

        # Icon
        image.paste(get_forecast_icon(day['icon']), (self.bounds[0], day_y))

        # Summary
        image_draw.text((self.bounds[0] + 55, day_y + 25), day['summary'], font = font, fill = 0)

        # Get day of the week for high/low
        future_day = datetime.date.today() + datetime.timedelta(days = index + 1)
        future_dotw = helpers.get_weekday_name(future_day.weekday())
        day_temps_str = f"{future_dotw}"
        image_draw.text((self.bounds[0] + 55, day_y), day_temps_str, font = font, fill = 0)

        # High/low
        high_low_str = f"{day['temp_high']}|{day['temp_low']}"
        image_draw.text((self.bounds[0] + 190, day_y), high_low_str, font = font, fill = 0)

        # Rain chance and wind speed for day
        precip_str = f"{day['precip_prob']}%"
        image_draw.text((self.bounds[0] + 260, day_y), precip_str, font = font, fill = 0)
        speed_str = f"{day['wind_speed']}mph"
        image_draw.text((self.bounds[0] + 335, day_y), speed_str, font = font, fill = 0)
    except Exception as err:
      self.set_error(err)
      self.draw_error(image_draw)

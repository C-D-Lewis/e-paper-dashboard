import os
import time
from datetime import datetime
from modules import fonts, config, helpers, epaper, timer
from widgets.WeatherWidget import WeatherWidget
from widgets.CryptoWidget import CryptoWidget
from widgets.NewsWidget import NewsWidget
from widgets.TwitterWidget import TwitterWidget
from widgets.ForecastWidget import ForecastWidget
from widgets.QuotesWidget import QuotesWidget
from widgets.SpotifyWidget import SpotifyWidget
from modules.constants import WIDGET_BOUNDS

# Slow data update interval
UPDATE_INTERVAL_M = 15
# Number of cycling widget pages
NUM_PAGES = 4

weather_widget = WeatherWidget()
crypto_widget = CryptoWidget()
spotify_widget = SpotifyWidget()
news_widget = NewsWidget()
forecast_widget = ForecastWidget()
twitter_widget = TwitterWidget()
quotes_widget = QuotesWidget()

################################### Drawing ####################################

#
# Draw time module
#
def draw_date_and_time(image_draw):
  root_x = 10
  root_y = 10

  now = datetime.now()
  time_str = now.strftime("%H:%M")
  image_draw.text((root_x, root_y), time_str, font = fonts.KEEP_CALM_80, fill = 0)
  date_str = now.strftime("%B %d, %Y")
  image_draw.text((root_x, root_y + 85), date_str, font = fonts.KEEP_CALM_48, fill = 0)

#
# Draw cycling page indicators
#
def draw_page_indicators(image_draw, page_index):
  root_x = 370
  root_y = 275
  gap_y = 25
  size = 8
  border = 2

  # For each dot
  for index in range(0, NUM_PAGES):
    shape_y = root_y + (index * gap_y)

    # Draw outer edge
    outer_shape = (
      root_x - border,
      shape_y - border,
      root_x + size + border,
      shape_y + size + border
    )
    image_draw.ellipse(outer_shape, fill = 0)

    # Fill if the selected one
    selected = page_index == index
    fill = 0 if selected else 1
    image_draw.ellipse((root_x, shape_y, root_x + size, shape_y + size), fill = fill)

#
# Draw all bounds for debugging purposes
#
def draw_all_bounds(image_draw):
  for index in range(0, len(WIDGET_BOUNDS)):
    helpers.draw_divider(image_draw, *WIDGET_BOUNDS[index])

################################## Main loop ###################################

#
# Draw things
#
def draw():
  timer.start()

  # Prepare
  image, image_draw = epaper.prepare()

  # Draw content
  weather_widget.draw(image_draw, image)
  draw_date_and_time(image_draw)

  # Top left
  spotify_widget.draw(image_draw, image)

  # Bottom left
  crypto_widget.draw(image_draw, image)

  # Dividers
  # Top from bottom
  helpers.draw_divider(image_draw, 0, 160, image.width, 5)
  # Left 'half' top from bottom
  helpers.draw_divider(image_draw, 0, 320, 350, 5)
  # Left 'half' from right 'half'
  helpers.draw_divider(image_draw, 350, 165, 5, 320)

  # Cycling widgets on the right side
  now = datetime.now()
  index = now.minute % NUM_PAGES
  if index == 0:
    news_widget.draw(image_draw, image)
  elif index == 1:
    forecast_widget.draw(image_draw, image)
  elif index == 2:
    twitter_widget.draw(image_draw, image)
  elif index == 3:
    quotes_widget.draw(image_draw, image)
  else:
    print(f"! Unused page index {index}")
  draw_page_indicators(image_draw, index)

  # Help debug bounds issues
  # draw_all_bounds(image_draw)

  # Update display
  epaper.show(image)
  timer.end('main draw')

  time.sleep(2)

#
# Update all data sources on a slow period
#
def periodic_data_update():
  weather_widget.update_data()
  crypto_widget.update_data()
  news_widget.update_data()
  forecast_widget.update_data()
  twitter_widget.update_data()
  quotes_widget.update_data()

#
# Minutely data source updates
#
def minutely_data_update():
  spotify_widget.update_data()

#
# Wait for the next minute
#
def wait_for_next_minute():
  now = datetime.now()
  while now.second != 1:
    now = datetime.now()
    time.sleep(1)

#
# The main function
#
def main():
  # Load config and prepare data once
  config.load()
  twitter_widget.resolve_user_name()

  # Initial update and draw
  timer.start()
  minutely_data_update()
  periodic_data_update()
  timer.end('initial update')
  epaper.init()
  draw()
  epaper.sleep()

  # Update once a minute forever
  while True:
    try:
      # Wait
      wait_for_next_minute()

      # Update data sources
      timer.start()
      minutely_data_update()
      if datetime.now().minute % UPDATE_INTERVAL_M == 0:
        periodic_data_update()
      timer.end('main update')

      with helpers.timeout(seconds=30):
        # Draw all widgets
        epaper.init()
        draw()
        epaper.sleep()
    except TimeoutError as err:
      # Display lock, reboot the system
      os.system('sudo reboot')
    except Exception as err:
      # Failed to work normally
      print(err)
      time.sleep(5)

if __name__ in '__main__':
  try:
    main()
  except KeyboardInterrupt:
    print('Exiting')
    epaper.deinit()
    exit()

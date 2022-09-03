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
from modules.constants import DIVIDER_SIZE, WIDGET_BOUNDS_BOTTOM_LEFT, WIDGET_BOUNDS_RIGHT, WIDGET_BOUNDS_TOP, WIDGET_BOUNDS_TOP_LEFT

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
  root_x = 8
  root_y = 10

  now = datetime.now()
  time_str = now.strftime("%H:%M")
  image_draw.text((root_x, root_y), time_str, font = fonts.KEEP_CALM_80, fill = 0)
  date_str = now.strftime("%B %d, %Y")
  image_draw.text((root_x, root_y + 87), date_str, font = fonts.KEEP_CALM_46, fill = 0)

#
# Draw cycling page indicators
#
def draw_page_indicators(image_draw, page_index):
  root_x = WIDGET_BOUNDS_TOP_LEFT[2] + 20
  root_y = 280
  gap_y = 25
  size = 8
  border = 2

  # Prevent spill from left hand side
  bg_x = 385
  bg_y = 167
  image_draw.rectangle([bg_x, bg_y, bg_x + 50, bg_y + 313], fill = 1)

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
# Draw all dividers between widgets
#
def draw_dividers(image_draw):
  # Top from bottom
  helpers.draw_divider(
    image_draw,
    0,
    WIDGET_BOUNDS_TOP[3],
    WIDGET_BOUNDS_TOP[2],
    DIVIDER_SIZE
  )
  # Left 'half' top from bottom
  divider_2_y = WIDGET_BOUNDS_TOP[3] + DIVIDER_SIZE + WIDGET_BOUNDS_TOP_LEFT[3]
  helpers.draw_divider(
    image_draw,
    0,
    divider_2_y,
    WIDGET_BOUNDS_TOP_LEFT[2],
    DIVIDER_SIZE
  )
  # Left 'half' from right 'half'
  divider_3_y = WIDGET_BOUNDS_TOP[3] + DIVIDER_SIZE
  helpers.draw_divider(
    image_draw,
    WIDGET_BOUNDS_TOP_LEFT[2],
    divider_3_y,
    DIVIDER_SIZE,
    WIDGET_BOUNDS_RIGHT[3]
  )

#
# Draw all bounds for debugging purposes
#
def draw_all_bounds(image_draw):
  helpers.draw_divider(image_draw, *WIDGET_BOUNDS_TOP_LEFT)
  helpers.draw_divider(image_draw, *WIDGET_BOUNDS_BOTTOM_LEFT)
  helpers.draw_divider(image_draw, *WIDGET_BOUNDS_RIGHT)

################################## Main loop ###################################

#
# Draw things
#
def draw():
  timer.start()

  # Prepare
  image, image_draw = epaper.prepare()

  # Top section
  weather_widget.draw(image_draw, image)
  draw_date_and_time(image_draw)

  # Left side
  spotify_widget.draw(image_draw, image)
  crypto_widget.draw(image_draw, image)

  # Decorations
  draw_dividers(image_draw)
  
  # Cycling widgets on the right side
  now = datetime.now()
  index = now.minute % NUM_PAGES
  index = 2
  draw_page_indicators(image_draw, index)
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

      with helpers.timeout(seconds=45):
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

import time
from datetime import datetime

from modules import fonts, config, helpers, epaper
from widgets.weather import WeatherWidget
from widgets.crypto import CryptoWidget
from widgets.news import NewsWidget
from widgets.rail import RailWidget
from widgets.twitter import TwitterWidget
from widgets.forecast import ForecastWidget
from widgets.quotes import QuotesWidget

# Constants
UPDATE_INTERVAL_M = 15
NUM_PAGES = 4

weather_widget = WeatherWidget()
crypto_widget = CryptoWidget()
rail_widget = RailWidget()
news_widget = NewsWidget()
forecast_widget = ForecastWidget()
twitter_widget = TwitterWidget()
quotes_widget = QuotesWidget()

################################### Drawing ####################################

# Draw time module
def draw_date_and_time(image_draw):
  root_x = 10
  root_y = 10

  now = datetime.now()
  time_str = now.strftime("%H:%M")
  image_draw.text((root_x, root_y), time_str, font = fonts.KEEP_CALM_80, fill = 0)
  date_str = now.strftime("%B %d, %Y")
  image_draw.text((root_x, root_y + 85), date_str, font = fonts.KEEP_CALM_48, fill = 0)

# Draw cycling page indicators
def draw_page_indicators(image_draw, page_index):
  root_x = 370
  root_y = 275
  gap_y = 25
  size = 8
  border = 2

  for index in range(0, NUM_PAGES):
    shape_y = root_y + (index * gap_y)

    outer_shape = (root_x - border, shape_y - border, root_x + size + border, shape_y + size + border)
    image_draw.ellipse(outer_shape, fill = 0)

    selected = page_index == index
    fill = 0 if selected else 1
    image_draw.ellipse((root_x, shape_y, root_x + size, shape_y + size), fill = fill)

################################## Main loop ###################################

# Draw things
def draw():
  # Prepare
  image, image_draw = epaper.prepare()

  # Draw content
  draw_date_and_time(image_draw)
  weather_widget.draw(image_draw, image)
  rail_widget.draw(image_draw, image)
  crypto_widget.draw(image_draw, image)
  helpers.draw_divider(image_draw, 0, 160, image.width, 5)
  helpers.draw_divider(image_draw, 0, 310, 350, 5)
  helpers.draw_divider(image_draw, 350, 165, 5, 320)

  # Cycling pages
  now = datetime.now()
  index = now.minute % NUM_PAGES
  if index == 0:
    news_widget.draw(image_draw, image)
  elif index == 1:
    forecast_widget.draw(image_draw, image)
  elif index == 2:
    twitter_widget.draw(image_draw, image)
  elif index == 3:
    quotes_widget.draw(image_draw)
  else:
    print(f"! Unused page index {index}")
  draw_page_indicators(image_draw, index)

  # Update display
  epaper.show(image)
  time.sleep(2)

# Update all data sources
def update_data_sources():
  weather_widget.update_data()
  rail_widget.update_data()
  crypto_widget.update_data()
  news_widget.update_data()
  forecast_widget.update_data()
  twitter_widget.update_data()
  quotes_widget.update_data()

# Wait for the next minute
def wait_for_next_minute():
  now = datetime.now()
  while now.second != 1:
    now = datetime.now()
    time.sleep(0.1)

# The main function
def main():
  config.load()
  twitter_widget.resolve_user_name()

  # Initial update
  update_data_sources()
  epaper.init()
  draw()
  epaper.sleep()

  # Update once a minute
  while True:
    try:
      wait_for_next_minute()

      if datetime.now().minute % UPDATE_INTERVAL_M == 0:
        update_data_sources()
      epaper.init()
      draw()
      epaper.sleep()
    except Exception as err:
      print(err)
      time.sleep(5)

if __name__ in '__main__':
  try:
    main()
  except KeyboardInterrupt:
    print('Exiting')
    epaper.deinit()
    exit()
